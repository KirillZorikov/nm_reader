<template>
  <header class="px-3 py-2 bg-dark text-white">
    <div class="wrapper mx-auto">
      <div
        class="
          d-flex
          flex-wrap
          col-12 col-md-auto
          align-items-center
          justify-content-center justify-content-md-start
        "
      >
        <a
          href="/"
          class="
            d-flex
            align-items-center
            mb-2 mb-lg-0
            text-white text-decoration-none
          "
          style="margin-top: -5px"
        >
          <svg
            data-v-20f285ec=""
            data-v-6b3fd699=""
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            class="text-currentColor icon"
          >
            <path
              data-v-20f285ec=""
              d="M3 12h12M3 6h18M3 18h6"
              stroke="white"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            ></path>
          </svg>
        </a>
        <a
          href="/"
          class="
            d-flex
            align-items-center
            mb-0
            ml-3
            text-white text-decoration-none
            me-auto
          "
        >
          <img src="../images/header.png" class="logo" alt="" />
        </a>
        <div
          class="
            input-group
            w-auto
            col-12 col-lg-auto
            mb-0
            me-lg-3
            search
            bg-white
            rounded-3
          "
        >
          <button
            class="btn btn-outline-secondary dropdown-toggle shadow-none"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            {{ current_dropdown }}
          </button>
          <ul class="dropdown-menu">
            <template v-for="(val, key) in dropdown" :key="key">
              <li>
                <a
                  class="dropdown-item"
                  :class="key === current_dropdown ? 'active' : ''"
                  @click="select_search(key)"
                >
                  {{ key }}
                </a>
              </li>
            </template>
            <li><hr class="dropdown-divider" /></li>
            <li>
              <a class="dropdown-item"
                ><i class="fas fa-cog"></i> Advanced Search</a
              >
            </li>
          </ul>
          <input
            v-model="search_val"
            type="text"
            class="form-control shadow-none"
            :placeholder="dropdown[current_dropdown]"
          />
          <button
            class="btn btn-outline-secondary shadow-none"
            @click="search(search_val, current_dropdown)"
          >
            <i
              class="fas fa-spinner fa-spin"
              style="font-weight: 600"
              v-if="loading"
            ></i>
            <i class="far fa-search" style="font-weight: 600" v-else></i>
            <!-- <i class="fas fa-spinner fa-pulse" style="font-weight: 600"></i> -->
          </button>
        </div>

        <div class="text-end bg-light p-1 rounded-circle text-center mb-0 ml-3">
          <a href="#" class="text-dark"><i class="far fa-user"></i></a>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { NovelService } from "../services/novel.service";

export default {
  name: "Header",

  RESOURCE_TO_ROUTE: {
    novel_page: "",
    search_page: "",
    author_page: "",
    chapter_page: {
      name: "NovelChapter",
      params: {
        service_name: "",
        lang_code: "",
        novel_id: "",
        chapter_id: "",
        data: "",
      },
    },
  },

  data() {
    return {
      loading: false,
      dropdown: {
        Link: "Try input a link on the author/title page",
        Novel: "Input keywords to search across all sites",
      },
      current_dropdown: "Link",
      search_val: "",
    };
  },
  methods: {
    select_search(key) {
      this.current_dropdown = key;
    },
    search(search_val, current_dropdown) {
      if (current_dropdown === "Link") {
        this.search_link(search_val);
      }
    },
    search_link(search_val) {
      this.loading = true;
      NovelService.getDataFromLink(search_val).then((response) => {
        this.loading = false;
        let resource = response.data.request_info.resource_name;
        console.log(resource);
        let keys = Object.keys(
          this.$options.RESOURCE_TO_ROUTE[resource].params
        );
        keys.forEach((key, index) => {
          this.$options.RESOURCE_TO_ROUTE[resource].params[key] =
            response.data.request_info[key];
        });
        this.$options.RESOURCE_TO_ROUTE[resource].params["data"] =
          JSON.stringify(response.data);
        console.log(this.$options.RESOURCE_TO_ROUTE[resource]);
        this.$router.push(this.$options.RESOURCE_TO_ROUTE[resource]);
      });
    },
  },
};
</script>

<style scoped>
.logo {
  max-height: 32px;
}
.search {
  min-width: 400px;
}
@media (max-width: 768px) {
  .search {
    min-width: 0;
    max-width: 200px;
  }
  .search button[data-bs-toggle="dropdown"] {
    display: none;
  }
  .search input {
    border-top-left-radius: 0.25rem !important;
    border-bottom-left-radius: 0.25rem !important;
  }
  .container {
    max-width: 650px !important;
  }
}
@media (max-width: 500px) {
  .search {
    max-width: 150px;
  }
}
@media (min-width: 768px) {
  .container {
    max-width: 900px;
  }
}
.text-end {
  height: 32px;
  width: 32px;
}
.dropdown-item {
  cursor: pointer;
}
.wrapper {
  max-width: 1222px;
}
</style>