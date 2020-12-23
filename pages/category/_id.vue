<template>
  <div>
    <v-sheet color="grey lighten-3">
      <v-container class="py-4">
        <h1>
          <template v-if="$i18n.locale === 'ja'">
            {{ label.startsWith('_') ? $t(label) : label }}を一覧する
          </template>
          <template v-else>
            {{ $t('browse_by') }}
            {{ label.startsWith('_') ? $t(label) : label }}
          </template>
        </h1>
      </v-container>
    </v-sheet>

    <v-container>
      <v-btn
        v-for="(value, index) in facetLabels"
        :key="index"
        class="my-1 mr-4"
        :to="
          localePath({
            name: 'category-id',
            params: {'id' : value},
          })
        "
      >
        {{ value.startsWith('_') ? $t(value) : value }}
      </v-btn>

      <v-sheet color="grey lighten-3 py-1 px-3 my-5">
        <v-row dense align="center">
          <v-col cols="12" sm="4" class="py-3"
            ><h3>
              {{ results.length.toLocaleString() }}{{ $t('hits') }}
            </h3></v-col
          >
        </v-row>
      </v-sheet>

      <v-row class="mb-5">
        <v-col
          v-for="(obj, index) in results"
          :key="index"
          :cols="6"
          :sm="2"
          class="my-2"
          style="word-break: break-word;"
        >
          <nuxt-link
            class="mr-2"
            :to="
              localePath({
                name: 'search',
                query: getParams('fc-'+label, obj.key),
              })
            "
          >
            {{ obj.key }}
          </nuxt-link>
          ({{ Number(obj.doc_count).toLocaleString() }})
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'

@Component({})
export default class PageCategory extends Vue {
  @Watch('$route', { deep: true })
  watchTmp(): void {
    this.search()
  }

  results: any[] = []
  label: string = ''

  facetLabels: any = {
    "冊": this.$t('冊'),
    "図": this.$t('図'),
    "水名": this.$t('水名'),
    "水経注：巻": this.$t('水経注：巻'),
  }

  // state
  mounted() {
    this.search()
  }

  async search() {
    const store = this.$store
    const routeQuery = this.$route.query

    if (store.state.index == null) {
      const index = await this.$searchUtils.loadIndex(
        process.env.BASE_URL + '/data/index.json'
      )
      this.$searchUtils.initStore(store, index)
    }

    if (Object.keys(store.state.facetLabels)) {
      store.commit('setFacetLabels', this.facetLabels)
    }

    let label: any = this.$route.params.id
    this.label = label

    // 検索
    const esQuery = this.$searchUtils.createQuery(routeQuery, store.state)
    const result = this.$searchUtils.search(
      store.state.index,
      store.state.data,
      esQuery
    )
    
    const results = result.aggregations[label].buckets
    this.results = results
  }

  head() {
    return {
      title: this.$t('category') + ' : ' + this.$t(this.label),
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: this.$t('search_by_category'),
        },
      ],
    }
  }

  getParams(label: string, value: string){
    const params: any = {}
    params[label] = value
    return params
  }
  

  
}
</script>
