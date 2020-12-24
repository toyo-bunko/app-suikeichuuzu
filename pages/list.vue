<template>
  <div>
    <v-sheet color="grey lighten-3">
      <v-container class="py-4">
        <h1>{{ $t('image_list') }}</h1>
      </v-container>
    </v-sheet>
    <v-container class="my-5">
      <v-row>
        <v-col cols="12" sm="4" v-for="(obj, key) in data" :key="key">
          <v-card no-body class="mb-4">
            <a :href="mirador + obj.manifest">
              <v-img
                :src="obj.image"
                contain
                style="height: 150px"
                width="100%"
                class="grey lighten-2"
              ></v-img>
            </a>

            <div class="pa-4">
              <a :href="mirador + obj.manifest">
                <b>{{ obj.title }}</b>
              </a>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mirador: process.env.BASE_URL + '/mirador?sidePanelOptions=on&manifest=',
      data: [
        {
          image:
            'https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/toyo/suikei/Suikeichuuzu_gousei_l.tif/full/200,/0/default.jpg',
          title: '本図',
          manifest:
            'https://nakamura196.github.io/suikeichuuzu/iiif/main/layer.json'
        }
      ]
    }
  },
  head() {
    const title = '画像一覧'
    return {
      title
    }
  }
}
</script>
