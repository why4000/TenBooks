---
name: engineering-cybernetics
description: "Knowledge base from 工程控制论 by 钱学森. Use when modeling dynamical systems with transfer functions, designing feedback loops, analyzing stability, handling time delays, random inputs, nonlinear servos, noise filtering, or adaptive and reliable control architectures."
---

# 工程控制论（新世纪版）
**Author**: 钱学森 (H. S. Tsien) | **Pages**: ~340 | **Chapters**: 18 | **Generated**: 2026-10-25

## How to Use This Skill

- **Without arguments** — load the core frameworks for control-system design
- **With a topic** — ask about `传递函数`, `反馈`, `稳定性`, `时滞`, `随机输入`, `非线性`, `自行镇定`, `误差控制`
- **With chapter** — ask for `ch04`; I load the feedback design criteria
- **With an engineering symptom** — describe 振荡、超调、反应慢、稳态误差、噪声大, and I map it to a chapter

---

## Core Frameworks & Mental Models

### 传递函数 (Transfer Function)
- **Use when** 需要把物理系统抽象成"输入—输出"关系，做频域分析或部件组合。
- 在零初始条件下，输出与输入的拉氏变换之比 `F(s)=Y(s)/X(s)`；它由极点、零点和放大系数完全刻画。
- **Key insight**: 不同物理本质的系统（弹簧、RC 电路）可以具有同一个传递函数，因此控制理论可以跨领域复用。

### 反馈 (Feedback)
- **Use when** 开环控制精度不够、反应太慢，或对象参数不确定。
- 测量输出、与输入比较得到偏差，再用偏差驱动执行机构；闭环传递函数为 `F1/(1+F1F2)`。
- **Key insight**: 反馈用"误差"代替"精确模型"，用高增益把参数敏感性和稳态误差压下去。

### 稳定性判定 (Stability Analysis)
- **Use when** 设计好回路后，必须回答"它会不会发散/持续振荡"。
- 线性系统稳定 ⇔ 闭环传递函数极点全在 s 左半平面；可用路斯—胡尔维茨代数判据或乃氏图围数判据。
- **Key insight**: 稳定性只看分母（特征方程），与输入无关；稳定性与快速性常常互相矛盾，需要折衷。

### 时滞系统 (Time-Lag Systems)
- **Use when** 传感器、执行器、燃烧或传输过程存在纯滞后。
- 时滞使系统成为微分差分方程，传递函数出现 `e^{-sτ}`，是超越函数；可用萨奇图把时滞项分离后套用乃氏判据。
- **Key insight**: 时滞不会改变稳态增益，却能摧毁稳定裕度；设计时要争取"对任意时滞都稳定"的绝对稳定性。

### 随机输入与功率谱 (Random Input & Power Spectrum)
- **Use when** 输入不可精确预知，只能用统计特性描述（湍流、噪声、起伏信号）。
- 用相关函数与功率谱刻画平稳随机过程，二者由维纳—辛钦关系互换；线性系统输出的功率谱等于输入功率谱乘 `|F(iω)|²`。
- **Key insight**: 对随机世界，设计目标不是"一条确定轨迹"，而是"输出的统计性质"。

### 非线性系统 (Nonlinear Systems)
- **Use when** 继电器、饱和、间隙、摩擦等使系统不满足叠加原理。
- 弱非线性可用小参数摄动展开；强非线性会出现极限环、跳跃、频率缩减、频率侵占、异步激发/抑制、参数激发。
- **Key insight**: 非线性系统可以同时"局部稳定"和"全局不稳定"；线性化只在工作点附近有效，接近共振时尤其危险。

### 自行镇定与适应环境 (Self-Stabilizing & Adaptive)
- **Use when** 系统复杂到无法预先枚举所有故障，或环境会持续变化。
- 在相空间设一条"可接受边界"，轨迹越界就切换参数；参数可随机试错，保留能回到稳定域的那一组。
- **Key insight**: 可靠性可以不靠"预先设计对"，而靠"越界就换参数"的机制自动搜索出来。

### 误差控制与冗余 (Error Control & Redundancy)
- **Use when** 元件本身不可靠，但系统整体必须可靠。
- 简单并联只能防"无输出"，防不了"错误输出"；冯·诺伊曼的复合方法用多路束、随机重排与复原机构把错误率压到任意低。
- **Key insight**: 冗余必须配"纠错结构"，否则只是把错误复制了多份。

### 解耦与不互相影响条件 (Decoupling)
- **Use when** 一个系统有多个被控制量，且它们互相牵动，单回路调参总是按下葫芦浮起瓢。
- 只有控制矩阵 `C` 可由设计者自由选定；令其非对角元素为零或由对角元素与发动机矩阵的余因式之比确定，即可使每个被控制量只受自己的给定值支配。
- **Key insight**: 耦合是结构问题而不是参数问题；解耦条件既必要又充分，对角元素仍可各自按第四章方法设计。

### 采样系统与施梯必茨—申南理论 (Sampled Data)
- **Use when** 反馈回路里有周期性闭合的采样开关，或信号只在离散时刻被处理。
- 把拉氏变换的积分换成求和，定义周期传递函数 `F2*(s)`，得到与连续系统同形的 `Y*=F1X*/(1+F1F2*)`；稳定判据仍是 `1+F1F2*` 不绕 `-1` 点。
- **Key insight**: 采样使稳定性条件放松（大部分时间没有反馈），但精度仍要求低频增益足够大。

### 极值搜索控制 (Extremum Seeking)
- **Use when** 对象的特性无法事先确知，或会因磨损、环境、结冰等缓慢漂移。
- 给输入叠加小幅周期性试探，测量输出的变化方向，据此反转输入方向，把系统维持在最优运转点附近；搜索损失与抗噪能力构成核心折衷。
- **Key insight**: 用"在线测量"替代"事先建模"，代价是输出围绕最优点持续小幅摆动。

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction.md) | 引言 | 系统分类, 工程近似 |
| [ch02](chapters/ch02-laplace-transform.md) | 拉氏变换法 | 拉氏变换, 初值问题 |
| [ch03](chapters/ch03-constant-coefficient-systems.md) | 常系数线性系统 | 传递函数, 频率特性 |
| [ch04](chapters/ch04-feedback-servomechanism.md) | 反馈伺服系统 | 反馈, 三条设计准则, 乃氏法 |
| [ch05](chapters/ch05-decoupling.md) | 不互相影响的控制 | 解耦, 反应方程 |
| [ch06](chapters/ch06-ac-and-oscillating-servo.md) | 交流伺服系统与振荡控制伺服系统 | 载波调制, 振荡线性化 |
| [ch07](chapters/ch07-sampled-data-systems.md) | 采样伺服系统 | 采样理论, Stibitz–Shannon |
| [ch08](chapters/ch08-time-lag-systems.md) | 有时滞的线性系统 | 微分差分方程, 萨奇图 |
| [ch09](chapters/ch09-random-input-systems.md) | 平稳随机输入下的线性系统 | 相关函数, 功率谱 |
| [ch10](chapters/ch10-relay-servo.md) | 继电器伺服系统 | 描述函数, 相平面, 最优开关 |
| [ch11](chapters/ch11-nonlinear-systems.md) | 非线性系统 | 弱非线性, 极限环, 频率侵占 |
| [ch12](chapters/ch12-variable-coefficient-systems.md) | 变系数线性系统 | 变系数, 贝塞尔方程 |
| [ch13](chapters/ch13-perturbation-design.md) | 利用摄动理论的控制设计 | 摄动方程, 伴随函数 |
| [ch14](chapters/ch14-integral-constraint-design.md) | 满足指定积分条件的控制设计 | 积分准则, 欧拉—拉格朗日 |
| [ch15](chapters/ch15-extremum-seeking.md) | 自动寻求最优运转点的控制系统 | 自寻最优, 搜索损失 |
| [ch16](chapters/ch16-noise-filtering.md) | 噪声过滤的设计原理 | 维纳滤波, 平均平方误差 |
| [ch17](chapters/ch17-self-stabilizing-adaptive.md) | 自行镇定和适应环境的系统 | 边界切换, 随机试错 |
| [ch18](chapters/ch18-error-control.md) | 误差的控制 | 冗余, 复合方法, 复原机构 |

## Topic Index

- **系统分类/工程近似** → ch01
- **拉氏变换/初值问题** → ch02
- **传递函数/伯德图/乃氏图** → ch03
- **反馈/开环 vs 闭环** → ch04
- **不互相影响的控制（解耦）** → ch05
- **交流伺服/振荡控制伺服** → ch06
- **采样伺服系统/Stibitz-Shannon** → ch07
- **时滞/火箭燃烧不稳定** → ch08
- **随机输入/白噪声** → ch09
- **继电器伺服/描述函数/相平面** → ch10
- **非线性/极限环** → ch11
- **变系数系统/火箭弹稳定性** → ch12
- **摄动理论控制设计/伴随函数** → ch13
- **指定积分条件的设计** → ch14
- **自动寻求最优运转点** → ch15
- **噪声过滤/维纳滤波** → ch16
- **自行镇定/适应环境** → ch17
- **可靠性/误差控制** → ch18

## Supporting Files

- [glossary.md](glossary.md) — key terms
- [patterns.md](patterns.md) — reusable design procedures
- [cheatsheet.md](cheatsheet.md) — quick reference (决策规则 + Tells & Smells)

---

## Scope & Limits
This skill covers the book's conceptual and methodological frameworks for engineering control. 原书 18 章已全覆盖（ch01–ch18），从传递函数、反馈伺服、时滞、随机输入，到非线性、采样、变系数、摄动设计、积分条件设计、极值搜索、噪声过滤与可靠性结构。原书成书于 1954 年，以连续时间、常系数线性系统、频域方法为主，未覆盖现代状态空间、鲁棒控制、LQR/MPC 等；公式部分 OCR 存在噪声，本产物只保留可可靠复原的结构、判据与方法步骤，具体数值计算与严格证明请回查原书对应章节或现代控制教材。
