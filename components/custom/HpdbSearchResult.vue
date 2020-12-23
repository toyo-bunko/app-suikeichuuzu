<template>
  <div>

    <v-card v-for="(obj, index) in results" :key="index" class="mb-5">
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="2">
            
            <nuxt-link
              :to="
                localePath({
                  name: 'item-id',
                  params: { id: obj._id },
                })
              "
            >
            <v-img
            :src="obj._source._thumbnail[0]"
            contain
            style="height: 150px"
            width="100%"
            class="grey lighten-2"
          ></v-img>
            </nuxt-link>
            
            
          </v-col>
          <v-col cols="12" sm="10">
            <h2>
              <nuxt-link
              :to="
                localePath({
                  name: 'item-id',
                  params: { id: obj._id },
                })
              "
            >
              {{ obj._source["地名/記述"][0] }}
              </nuxt-link>
            </h2>
            <p class="mt-2">
              <b>{{$t("冊")}}:</b> {{ obj._source["冊"][0] }}
              <b class="ml-2">{{$t("図")}}:</b> {{ obj._source["図"][0] }}
            </p>
            <div class="text-right">
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    icon
                    class="mt-2"
                    target="_blank"
                    :href="obj._source._relatedLink[0]"
                    v-on="on"
                    ><img
                      :src="baseUrl + '/img/icons/icp-logo.svg'"
                      width="30px"
                  /></v-btn>
                </template>
                <span>{{ 'IIIF Curation Viewer' }}</span>
              </v-tooltip>

              
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'

@Component({
  components: {},
})
export default class ListSearchResult extends Vue {
  baseUrl: string = process.env.BASE_URL || ''

  get results() {
    return this.$store.state.result.hits.hits
  }

  get query() {
    return this.$store.state.query
  }

  get selected() {
    return this.$store.state.selected
  }

  set selected(value) {
    this.$store.commit('setSelected', value)
  }

  selectedTemporary: string[] = []

  dialog: boolean = false

  get index() {
    return this.$store.state.index
  }

  get dataAll() {
    return this.$store.state.data
  }

  select(id: string) {
    const selected = JSON.parse(JSON.stringify(this.selected))
    const index = selected.indexOf(id)
    if (index === -1) {
      selected.push(id)
    } else if (index !== -1) {
      selected.splice(index, 1)
    }
    this.selected = selected
  }

  compare() {
    const param = []

    for (let i = 0; i < this.selected.length; i++) {
      const id = this.selected[i]
      const obj = this.getLabel(id)
      const related = obj._source._relatedLink[0]

      const relatedSpl = related.split('&')
      const manifest = relatedSpl[0].split('=')[1]

      const canvas =
        relatedSpl[1].split('=')[1] + '#xywh=' + relatedSpl[2].split('=')[1]

      param.push({
        manifest,
        canvas,
      })
    }

    const url =
      this.baseUrl +
      '/mirador/?params=' +
      encodeURIComponent(JSON.stringify(param)) +
      '&layout=' +
      this.selected.length +
      'x1'
    open(url, '_blank')
  }

  resetSelected() {
    this.selected = []
    const hits = this.results.hits.hits
    for (let i = 0; i < hits.length; i++) {
      const obj = hits[i]
      obj.selected = false
    }
  }

  deleteSelected() {
    const selectedTemporary = this.selectedTemporary
    const selected = JSON.parse(JSON.stringify(this.selected))
    for (let i = 0; i < selectedTemporary.length; i++) {
      const id = selectedTemporary[i]
      const index = selected.indexOf(id)
      selected.splice(index, 1)
    }

    this.selected = selected
    this.selectedTemporary = []
  }

  getLabel(id: string) {
    const seq = this.index._id[id][0]
    const obj = this.dataAll[seq]
    return obj
  }

}
</script>
