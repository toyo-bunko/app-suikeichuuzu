<template>
  <div>

    <p class="text-right">
      <v-btn :href="map" target="_blank" color="primary">{{$t("view_map")}}</v-btn>
    </p>

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
  map: string = ""

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

  mounted(){
    const results = this.results
    //const members = []
    let url = "/etc/?curation=/data/curation.json"
    for(let i = 0; i < results.length; i++){
      const related = results[i]._source._relatedLink[0].split("&")
      const member_id = related[1].split("=")[1] + "#" + related[2]
      //members.push(member_id)
      url += "&member="+encodeURIComponent(member_id)
    }
    //const url = "/etc/?curation=/data/curation.json&members="+encodeURIComponent(members)
    this.map = url
  }

  getLabel(id: string) {
    const seq = this.index._id[id][0]
    const obj = this.dataAll[seq]
    return obj
  }

}
</script>
