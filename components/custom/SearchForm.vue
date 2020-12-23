<template>
  <v-container class="pt-5">
    <v-card class="my-5" flat outlined>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="3">
            <v-select
              v-model="vol"
              :items="vols"
              :label="$t('冊')"
              multiple
            ></v-select>
          </v-col>

          <v-col cols="12" sm="3">
            <v-select
              v-model="pic"
              :items="pics"
              :label="$t('図')"
              multiple
            ></v-select>
          </v-col>

          <v-col cols="12" sm="3">
            <v-select
              v-model="sn"
              :items="sns"
              :label="$t('区画南北')"
              multiple
            ></v-select>
          </v-col>

          <v-col cols="12" sm="3">
            <v-select
              v-model="ew"
              :items="ews"
              :label="$t('区画東西')"
              multiple
            ></v-select>
          </v-col>

          <v-col cols="12" sm="3">
            <v-select
              v-model="fb"
              :items="fbs"
              :label="$t('表裏')"
              multiple
            ></v-select>
          </v-col>

          <v-col cols="12" sm="3">
            <v-select
              v-model="detail"
              :items="details"
              :label="$t('詳細区画')"
              multiple
            ></v-select>
          </v-col>

          <v-col cols="12" sm="3">
            <v-select
              v-model="red"
              :items="reds"
              :label="$t('墨朱')"
              multiple
            ></v-select>
          </v-col>

          <v-col cols="12" sm="3">
            <v-select
              v-model="mark"
              :items="marks"
              :label="$t('記号')"
              multiple
            ></v-select>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="location"
              :label="$t('地名/記述')"
              @keyup.enter="search"
            ></v-text-field>
            <!-- class="phone" -->
          </v-col>

          <v-col cols="12" sm="3">
            <v-text-field
              v-model="remark"
              :label="$t('備考')"
              @keyup.enter="search"
            ></v-text-field>
            <!-- class="phone" -->
          </v-col>

          <v-col cols="12" sm="3">
            <v-btn class="ma-2" color="primary" @click="search">{{
              $t('search')
            }}</v-btn>
            <v-btn class="ma-2" @click="reset">{{ $t('reset') }}</v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'nuxt-property-decorator'

@Component({})
export default class SearchForm extends Vue {
  vols: string[] = ['1', '2', '3', '4']

  pics: string[] = ['本図']
  
  sns: string[] = ['南5', '南4', '南3', '南2', "南1", "中", "北1", "北2", "北3", "北4", "北5"]
  
  ews: string[] = ["東6", '東5', "東4", '東3', '東2', "東1", 
  "中", "西1", "西2", "西3", "西4", "西5", "西6", "西7", "西8", "西9", "西10", "西11", "西12"]
  
  fbs: string[] = ["表", "裏"]

  details: string[] = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "D1", "D2", "D3"]

  reds: string[] = ["墨", "朱"]

  marks: string[] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

  mounted() {
    this.init()
  }

  @Watch('$route')
  watchRoute(): void {
    this.init()
  }

  init() {
    const advanced = this.$route.query

    if (advanced['fc-冊']) {
      const vols = advanced['fc-冊']
      this.vol = Array.isArray(vols) ? vols : [vols]
    } else {
      this.vol = []
    }

    if (advanced['fc-図']) {
      const values = advanced['fc-図']
      this.pic = Array.isArray(values) ? values : [values]
    } else {
      this.pic = []
    }

    if (advanced['fc-区画南北']) {
      const values = advanced['fc-区画南北']
      this.sn = Array.isArray(values) ? values : [values]
    } else {
      this.sn = []
    }

    if (advanced['fc-区画東西']) {
      const values = advanced['fc-区画東西']
      this.ew = Array.isArray(values) ? values : [values]
    } else {
      this.ew = []
    }

    if (advanced['fc-表裏']) {
      const values = advanced['fc-表裏']
      this.fb = Array.isArray(values) ? values : [values]
    } else {
      this.fb = []
    }

    if (advanced['fc-詳細区画']) {
      const values = advanced['fc-詳細区画']
      this.detail = Array.isArray(values) ? values : [values]
    } else {
      this.detail = []
    }

    if (advanced['fc-墨朱']) {
      const values = advanced['fc-墨朱']
      this.red = Array.isArray(values) ? values : [values]
    } else {
      this.red = []
    }

    if (advanced['fc-図記号']) {
      const values = advanced['fc-図記号']
      this.mark = Array.isArray(values) ? values : [values]
    } else {
      this.mark = []
    }

    if (advanced['q-地名/記述']) {
      this.location = advanced['q-地名/記述']
    } else {
      this.location = ''
    }

    if (advanced['q-備考']) {
      this.remark = advanced['q-備考']
    } else {
      this.remark = ''
    }
  }

  vol: any = []

  pic: string[] = []

  sn: string[] = []

  ew: string[] = []

  fb: string[] = []

  detail: string[] = []

  red: string[] = []

  mark: any = []

  location: string = ''

  remark: string = ""

  get advanced() {
    return this.$store.state.advanced
  }

  search() {
    const query: any = {}

    // --------

    const vol = this.vol

    if (vol.length !== 0) {
      query['fc-冊'] = vol
    }

    const pic = this.pic

    if (pic.length !== 0) {
      query['fc-図'] = pic
    }

    const sn = this.sn

    if (sn.length !== 0) {
      query['fc-区画南北'] = sn
    }

    const ew = this.ew

    if (ew.length !== 0) {
      query['fc-区画東西'] = ew
    }

    const fb = this.fb

    if (fb.length !== 0) {
      query['fc-表裏'] = fb
    }

    const detail = this.detail

    if (detail.length !== 0) {
      query['fc-詳細区画'] = detail
    }

    const red = this.red

    if (red.length !== 0) {
      query['fc-墨朱'] = red
    }

    const mark = this.mark

    if (mark.length !== 0) {
      query['fc-図記号'] = mark
    }

    const location = this.location
    if (location !== '') {
      query['q-地名/記述'] = location
    }

    const remark = this.remark
    if (remark !== '') {
      query['fc-備考'] = remark
    }

    // --------

    this.$router.push(
      this.localePath({
        name: 'search',
        query,
      }),
      () => {},
      () => {}
    )
  }

  reset() {
    this.$router.push(
      this.localePath({
        name: 'search',
      }),
      () => {},
      () => {}
    )
  }
}
</script>
