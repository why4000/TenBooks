const { createApp, ref, computed, reactive, onMounted } = Vue;

const app = createApp({
  setup() {
    const books = ref(window.SKILL_DATA?.books || []);
    const activeBook = ref(books.value[0]?.slug || null);
    const keyword = ref("");
    const filterBook = ref("all");

    const panels = reactive({
      books: true, tree: true, frameworks: true,
      chapters: false, caps: true, glossary: false
    });
    const openChapters = reactive({});

    const activeBookObj = computed(() =>
      books.value.find(b => b.slug === activeBook.value)
    );

    const filteredBooks = computed(() => {
      if (!keyword.value.trim()) return books.value;
      const kw = keyword.value.toLowerCase();
      return books.value.filter(b => {
        return b.title.toLowerCase().includes(kw)
          || b.author.toLowerCase().includes(kw)
          || b.type.toLowerCase().includes(kw)
          || b.frameworks.some(f => f.name.toLowerCase().includes(kw)
               || (f.desc || "").toLowerCase().includes(kw)
               || (f.use_when || "").toLowerCase().includes(kw))
          || b.capabilities.some(c => (c.one_liner || "").toLowerCase().includes(kw)
               || (c.description || "").toLowerCase().includes(kw)
               || (c.keywords || []).some(k => k.toLowerCase().includes(kw)))
          || b.glossary.some(g => g.term.toLowerCase().includes(kw)
               || (g.def || "").toLowerCase().includes(kw))
          || b.chapters.some(ch => (ch.title || "").toLowerCase().includes(kw)
               || (ch.core || "").toLowerCase().includes(kw));
      });
    });

    const filteredFrameworks = computed(() => {
      if (!activeBookObj.value) return [];
      if (!keyword.value.trim()) return activeBookObj.value.frameworks;
      const kw = keyword.value.toLowerCase();
      return activeBookObj.value.frameworks.filter(f =>
        f.name.toLowerCase().includes(kw)
        || (f.desc || "").toLowerCase().includes(kw)
        || (f.use_when || "").toLowerCase().includes(kw)
      );
    });

    const filteredGlossary = computed(() => {
      if (!activeBookObj.value) return [];
      if (!keyword.value.trim()) return activeBookObj.value.glossary;
      const kw = keyword.value.toLowerCase();
      return activeBookObj.value.glossary.filter(g =>
        g.term.toLowerCase().includes(kw) || g.def.toLowerCase().includes(kw)
      );
    });

    // 能力调用链树: promoted 为根，router 为子节点
    const capTree = computed(() => {
      if (!activeBookObj.value) return [];
      const caps = activeBookObj.value.capabilities;
      const promoted = caps.filter(c => c.destination === "promoted");
      const router = caps.filter(c => c.destination !== "promoted");
      const tree = [];
      promoted.forEach(p => {
        tree.push({
          id: p.capability_id,
          name: p.one_liner || p.capability_id,
          type: "promoted",
          children: router.map(r => ({
            id: r.capability_id,
            name: r.one_liner || r.capability_id,
            type: r.destination || "router",
            children: []
          }))
        });
      });
      // 如果没有 promoted，把 router 放顶层
      if (promoted.length === 0) {
        router.forEach(r => {
          tree.push({ id: r.capability_id, name: r.one_liner || r.capability_id, type: "router", children: [] });
        });
      }
      return tree;
    });

    function togglePanel(key) {
      panels[key] = !panels[key];
    }

    function selectBook(slug) {
      activeBook.value = slug;
      // 重置章节展开
      Object.keys(openChapters).forEach(k => delete openChapters[k]);
      // 滚动到顶部
      document.querySelector(".content")?.scrollTo(0, 0);
    }

    function toggleChapter(file) {
      openChapters[file] = !openChapters[file];
    }

    function jumpToCap(capId) {
      const el = document.getElementById("cap-" + activeBook.value + "-" + capId);
      if (el) {
        panels.caps = true;
        el.scrollIntoView({ behavior: "smooth", block: "center" });
        el.style.background = "rgba(99,102,241,0.2)";
        setTimeout(() => { el.style.background = ""; }, 1500);
      }
    }

    return {
      books, activeBook, keyword, filterBook, panels, openChapters,
      activeBookObj, filteredBooks, filteredFrameworks, filteredGlossary, capTree,
      togglePanel, selectBook, toggleChapter, jumpToCap
    };
  }
});

// 树节点组件
app.component("tree-node", {
  props: ["node", "level"],
  emits: ["select"],
  template: `
    <div class="tree-node">
      <div class="tree-node-name" :class="node.type" @click="$emit('select', node.id)">
        {{ node.name }}
      </div>
      <div class="tree-children" v-if="node.children && node.children.length">
        <tree-node v-for="c in node.children" :key="c.id" :node="c" :level="level+1"
                   @select="$emit('select', $event)"></tree-node>
      </div>
    </div>
  `
});

app.mount("#app");
