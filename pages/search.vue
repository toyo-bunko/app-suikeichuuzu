<template>
  <div>
    <template v-if="loadingFlag">
      <div class="text-center my-10">
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </div>
    </template>
    <template v-else>
      <SearchForm />

      <v-sheet color="grey lighten-3">
        <SearchFilter />
      </v-sheet>

      <v-container fluid>
        <ResultHead
          :sort-options="sortOptions"
          :layout-options="layoutOptions"
        />
        <Result />
      </v-container>
    </template>
  </div>
</template>

<script lang="ts">
import axios from "axios"
import { Vue, Component, Watch } from 'nuxt-property-decorator'
import SearchForm from '~/components/custom/SearchForm.vue'

import SearchFilter from '~/components/custom/CustomFilter.vue'
import Result from '~/components/search/Result.vue'
import ResultHead from '~/components/search/ResultHead.vue'

@Component({
  components: {
    SearchForm,
    SearchFilter,
    Result,
    ResultHead,
  },
})
export default class search extends Vue {
  // 設定
  sortOptions: any[] = [
    {
      value: '冊:asc',
      text: this.$t('冊') + ' ' + this.$t('asc'),
    },
    {
      value: '冊:desc',
      text: this.$t('冊') + ' ' + this.$t('desc'),
    },
  ]

  layoutOptions: any[] = [
    { value: 'hpdb', text: 'default' },
    { value: 'grid', text: 'grid' },
    { value: 'image', text: 'thumbnail' },
    { value: 'table', text: 'table' },
    { value: 'stats', text: 'graph' },
  ]

  facetLabels: any = {
    "冊": this.$t('冊'),
    "図": this.$t('図'),
    "水名": this.$t('水名'),
    "水経注：巻": this.$t('水経注：巻'),
  }

  facetFlags: string[] = [
    "冊",
    "図",
    '水名',
    '水経注：巻'
  ]

  dict: any = {}

  loadingFlag: boolean = true

  // state
  mounted() {
    this.search()
  }

  @Watch('$route')
  watchRoute(): void {
    this.search()
  }

  async search() {
    const store = this.$store
    const routeQuery = this.$route.query

    // 初期化
    if (!routeQuery.sort) {
      routeQuery.sort = '冊:asc'
    }
    if (!routeQuery.layout) {
      routeQuery.layout = 'hpdb'
    }
    this.loadingFlag = true
    store.commit('init', routeQuery)

    // ------ インデックス ---------

    if (store.state.index == null) {
      const index = await this.$searchUtils.loadIndex(
        process.env.BASE_URL + '/data/index.json'
      )
      this.$searchUtils.initStore(store, index)

      const dd = await axios.get(
        process.env.BASE_URL + '/data/dict.json'
      ).then((res)=> {
        return res.data
      })
      store.commit('setDictionary', dd)
    }

    // ------ ファセット ---------

    if (Object.keys(store.state.facetLabels)) {
      store.commit('setFacetLabels', this.facetLabels)
      store.commit('setFacetFlags', this.facetFlags)
    }

    const dd = store.state.dictionary

    if(routeQuery["q-地名"]){
      let location: any = routeQuery["q-地名"]
      for(let key in dd){
        location = location.replace(key, dd[key])
      }
      routeQuery["q-地名"] = location
    }

    // 検索
    const esQuery = this.$searchUtils.createQuery(routeQuery, store.state)
    const result = this.$searchUtils.search(
      store.state.index,
      store.state.data,
      esQuery
    )
    this.$store.commit('setResult', result)

    // --------------- ここまで elatic search ---------------

    this.loadingFlag = false
  }

  head() {
    return {
      title: this.$t('search'),
    }
  }
}
</script>
