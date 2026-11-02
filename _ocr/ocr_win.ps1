param(
    [Parameter(Mandatory=$true)][string]$ImageDir,
    [Parameter(Mandatory=$true)][string]$OutFile,
    [string]$Lang = "zh-Hans-CN"
)

Add-Type -AssemblyName System.Runtime.WindowsRuntime

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
})[0]

function Await($WinRtTask, $ResultType) {
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}

[void][Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime]
[void][Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics, ContentType=WindowsRuntime]
[void][Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime]
[void][Windows.Globalization.Language, Windows.Globalization, ContentType=WindowsRuntime]

$language = New-Object Windows.Globalization.Language($Lang)
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($language)
if ($null -eq $engine) {
    Write-Error "Cannot create OCR engine for $Lang"
    exit 1
}

$files = Get-ChildItem -Path $ImageDir -Filter *.png | Sort-Object Name
Write-Host "OCR engine ready. Files: $($files.Count)"

$sw = [System.Diagnostics.Stopwatch]::StartNew()
$writer = New-Object System.IO.StreamWriter($OutFile, $false, (New-Object System.Text.UTF8Encoding($false)))
$i = 0
try {
    foreach ($f in $files) {
        $i++
        try {
            $sf = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($f.FullName)) ([Windows.Storage.StorageFile])
            $stream = Await ($sf.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
            $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
            $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
            $result = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])

            $writer.WriteLine("===== PAGE " + $f.BaseName + " =====")
            foreach ($line in $result.Lines) {
                $writer.WriteLine($line.Text)
            }
            $writer.WriteLine("")

            $bitmap.Dispose()
            $stream.Dispose()
        } catch {
            $writer.WriteLine("===== PAGE " + $f.BaseName + " [OCR_ERROR: " + $_.Exception.Message + "] =====")
            $writer.WriteLine("")
        }

        if ($i % 10 -eq 0) {
            $el = $sw.Elapsed.TotalSeconds
            Write-Host ("  {0}/{1} pages, elapsed {2:N0}s, avg {3:N2}s/page" -f $i, $files.Count, $el, ($el/$i))
        }
    }
} finally {
    $writer.Close()
    $sw.Stop()
}

Write-Host ("DONE: {0} pages in {1:N0}s -> {2}" -f $i, $sw.Elapsed.TotalSeconds, $OutFile)
