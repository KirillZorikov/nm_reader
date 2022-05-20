<template>
  <SideBarChapter />
  <div class="top text-center">
    <a href="" class="title"
      ><h1 v-if="text_data.orig_title">
        {{ text_data.tr_text[text_data.orig_title] }}
      </h1></a
    >
    <div class="col-lg-6 mx-auto">
      <p class="chapter-name mb-4">
        {{ text_data.tr_text[text_data.orig_chapter_name] }}
      </p>
      <div class="d-flex justify-content-center">
        <button
          type="button"
          class="button-top px-4"
          @click="clickNavigation('prev')"
        >
          <i class="fas fa-angle-left fs-6 align-middle"></i> Prev Chapter
        </button>
        <button
          type="button"
          class="button-top"
          data-bs-toggle="offcanvas" data-bs-target="#offcanvas" role="button"
        >
          <i class="fas fa-cog"></i>
        </button>


        <button type="button" class="button-top">
          <i class="fas fa-list"></i>
        </button>
        <button
          type="button"
          class="button-top px-4 ml-4"
          @click="clickNavigation('next')"
        >
          Next Chapter <i class="fas fa-angle-right fs-6 align-middle"></i>
        </button>
      </div>
      <div class="text-start px-5 d-flex justify-content-center">
        <img src="../images/chapter-start.webp" />
      </div>
    </div>
  </div>

  <div class="text py-4">
    <Loading
      :message="'Load chapter '"
      v-if="loading"
      class="loading_message my-4"
    />
    <template v-if="!loading">
      <p v-for="p in text_data.orig_text" :key="p">
        {{ text_data.tr_text[p] ? text_data.tr_text[p] : p }}
      </p>
    </template>
    <template v-if="author_note && !loading">
      <hr class="mx-4" />
      <p v-for="p in text_data.orig_author_note" :key="p">
        {{ text_data.tr_text[p] ? text_data.tr_text[p] : p }}
      </p>
    </template>
  </div>

  <div class="bottom mx-auto">
    <div class="d-flex justify-content-center align-items-center flex-column">
      <div class="text-start">
        <img src="../images/chapter-end.webp" />
      </div>
      <div class="d-flex justify-content-center">
        <button
          type="button"
          class="button-top px-4 ml-0"
          @click="clickNavigation('prev')"
        >
          <i class="fas fa-angle-left fs-6 align-middle"></i> Prev Chapter
        </button>
        <button type="button" class="button-top">
          <i class="fas fa-list"></i>
        </button>
        <button
          type="button"
          class="button-top px-4 ml-4 mr-0"
          @click="clickNavigation('next')"
        >
          Next Chapter <i class="fas fa-angle-right fs-6 align-middle"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { NovelService } from "../services/novel.service";
import { TranslateService } from "../services/translate.services";
import SideBarChapter from "../components/SideBarChapter.vue";
import Loading from "../components/Loading";

export default {
  name: "NovelChapter",
  components: { Loading, SideBarChapter },
  props: {
    service_name: String,
    lang_code: String,
    novel_id: String,
    chapter_id: String,
    data: String,
  },
  data() {
    return {
      loading: false,
      response_data: "",
      text_arr: [],
      author_note_arr: [],
      tr_text: {},
      orig_text: [],
      orig_author_note: [],
      text_data: {
        orig_text: [],
        orig_author_note: [],
        orig_title: "",
        orig_chapter_name: "",
        tr_text: {},
      },
    };
  },
  computed: {
    title() {
      let title;
      if (this.response_data) {
        title =
          "title_link" in this.response_data
            ? this.response_data.title_link.text
            : this.response_data.title;
      }
      return title;
    },
    name() {
      return this.response_data.name;
    },
    text() {
      let text;
      if (this.response_data) {
        this.text_arr = this.response_data.text.split("\n");
        this.text_arr.forEach((element, index) => {
          if (element) {
            this.text_arr[index] = `<p>${element.trim()}</p>`;
          }
        });
        text = this.text_arr.join("");
      }
      return text;
    },
    author_note() {
      let author_note;
      if (this.response_data.author_note) {
        this.author_note_arr = this.response_data.author_note.split("\n");
        this.author_note_arr.forEach((element, index) => {
          if (element) {
            this.author_note_arr[index] = `<p>${element.trim()}</p>`;
          }
        });
        author_note = this.author_note_arr.join("");
      }
      return author_note;
    },
    next_link() {
      let next_link;
      if (this.response_data.next) {
        next_link = this.response_data.next;
      }
      return next_link;
    },
    prev_link() {
      let prev_link;
      if (this.response_data.prev) {
        prev_link = this.response_data.prev;
      }
      return prev_link;
    },
  },
  created() {
    if (this.data) {
      this.response_data = JSON.parse(this.data);
      this.saveText(this.response_data);
      console.log(this.text_data.tr_text);
      this.translateChapter("deepl", Object.keys(this.text_data.tr_text), 4);
    } else {
      this.loadChapter();
    }
  },
  methods: {
    loadChapter() {
      this.loading = true;
      NovelService.getChapter(
        this.lang_code,
        this.service_name,
        this.novel_id,
        this.chapter_id
      ).then((response) => {
        this.response_data = response.data;
        this.saveText(response.data);
        this.translateChapter("deepl", Object.keys(this.text_data.tr_text), 4);
      });
    },
    loadChapterFromUrl(url) {
      this.loading = true;
      NovelService.getDataFromLink(url).then((response) => {
        this.response_data = response.data;
        this.saveText(response.data);
        this.translateChapter("deepl", Object.keys(this.text_data.tr_text), 4);
      });
    },
    saveText(data) {
      this.text_data.orig_text = data.text.split("\n").filter((n) => n);
      this.text_data.orig_author_note = data.author_note? data.author_note
        .split("\n")
        .filter((n) => n): [];
      this.text_data.orig_title =
        "title" in data ? data.title : data.title_link.text;
      this.text_data.orig_chapter_name = data.name;
      this.text_data.orig_text
        .concat(this.text_data.orig_author_note)
        .forEach((e, i) => {
          this.text_data.tr_text[e] = "";
        });
      this.text_data.tr_text[this.text_data.orig_title] = "";
      this.text_data.tr_text[data.name] = "";
    },
    clickNavigation(type) {
      if (type === "next" && this.next_link) {
        this.loadChapterFromUrl(this.next_link);
      } else if (type === "prev" && this.prev_link) {
        this.loadChapterFromUrl(this.prev_link);
      }
    },
    translateChapter(service, paragraphs, parts = 4) {
      if (!paragraphs.length) {
        return;
      }
      let chunks = this.splitToChunks([...paragraphs], parts);
      TranslateService.initPages(service).then((response) => {
        let data = { src: "auto", dst: "ru" };
        chunks.forEach((chunk, index) => {
          TranslateService.getTranslate(
            { ...data, paragraphs: chunk },
            service
          ).then((response) => {
            chunk.forEach((p, index) => {
              this.text_data.tr_text[p] = response.data[index];
            });
            this.loading = false;
          });
        });
      });
    },
    splitToChunks(array, parts) {
      let result = [];
      for (let i = parts; i > 0; i--) {
        result.push(array.splice(0, Math.ceil(array.length / i)));
      }
      return result;
    },
  },
};
</script>

<style scoped>
.m-card.search {
  min-height: 50vh;
  margin-top: 100px;
}
.chapter-name {
  color: #555;
  font-size: 18px;
}
.title {
  display: inline-block;
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
  text-shadow: 0 0 1px #c2c2c2;
  text-align: center;
  color: #3974a9;
  text-decoration: none;
}
.button-top {
  overflow: hidden;
  display: block;
  padding: 0 12px;
  line-height: 32px;
  font-size: 14px;
  color: #fff;
  background-color: #14425d;
  border: 1px solid #14425d;
  margin: 0 3px;
}
.text-start img {
  margin: 15px 0 19px;
  max-width: 200px;
}
.text {
  border-top: 1px solid #dcdcdc;
  border-bottom: 1px solid #dcdcdc;
  min-height: 50vh;
}
</style>
