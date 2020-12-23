<template>
  <div>
    <v-container class="py-5">
      <iframe
        :src="getIframeUrl()"
        width="100%"
        height="400"
        allowfullscreen
        frameborder="0"
      ></iframe>
    </v-container>
    <v-container>
      <p class="text-center">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              class="mx-1"
              icon
              target="_blank"
              :href="getCurationUrl()"
              v-on="on"
              ><img :src="baseUrl + '/img/icons/icp-logo.svg'" width="30px"
            /></v-btn>
          </template>
          <span>{{ 'IIIF Curation Viewer' }}</span>
        </v-tooltip>

        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              class="mx-1"
              icon
              target="_blank"
              :href="'https://twitter.com/intent/tweet?url=' + url"
              v-on="on"
              ><v-icon>mdi-twitter</v-icon></v-btn
            >
          </template>
          <span>{{ 'Twitter' }}</span>
        </v-tooltip>

        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              class="mx-1"
              icon
              target="_blank"
              :href="'https://www.facebook.com/sharer/sharer.php?u=' + url"
              v-on="on"
              ><v-icon>mdi-facebook</v-icon></v-btn
            >
          </template>
          <span>{{ 'Facebook' }}</span>
        </v-tooltip>

        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              class="mx-1"
              icon
              target="_blank"
              :href="'http://getpocket.com/edit?url=' + url"
              v-on="on"
              ><img
                style="font-size: 30px"
                src="https://cultural.jp/img/icons/pocket.svg"
            /></v-btn>
          </template>
          <span>{{ 'Pocket' }}</span>
        </v-tooltip>
      </p>
      <dl class="row">
        <dt class="col-sm-3 text-muted"><b>URL</b></dt>
        <dd class="col-sm-9">
          <a :href="url">{{
            url
          }}</a>
        </dd>
      </dl>

      <dl class="row">
        <dt class="col-sm-3 text-muted">
          <b>{{ $t('label') }}</b>
        </dt>
        <dd class="col-sm-9">
          {{ title }}
        </dd>
      </dl>

      <dl v-for="(obj, key) in metadata" :key="key" class="row">
        <template
          v-if="
            fields.includes(obj.label)
          "
        >
          <dt class="col-sm-3 text-muted">
            <b>{{ $t(obj.label) }}</b>
          </dt>
          <dd
            class="col-sm-9"
            :class="obj.label === 'Phone/Word' ? 'phone' : ''"
          >
            {{ Array.isArray(obj.value) ? obj.value.join(', ') : obj.value }}
          </dd>
        </template>
      </dl>

      <dl class="row">
        <dt class="col-sm-3 text-muted">
          <b>{{ $t('license') }}</b>
        </dt>
        <dd class="col-sm-9">
          <template v-if="$i18n.locale == 'ja'">
            <a rel="license" href="http://creativecommons.org/licenses/by/4.0/"
              ><img
                alt="クリエイティブ・コモンズ・ライセンス"
                style="border-width: 0"
                src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a
            ><br />この作品は<a
              rel="license"
              href="http://creativecommons.org/licenses/by/4.0/"
              >クリエイティブ・コモンズ 表示 4.0 国際 ライセンス</a
            >の下に提供されています。
          </template>
          <template v-else>
            <a rel="license" href="http://creativecommons.org/licenses/by/4.0/"
              ><img
                alt="Creative Commons License"
                style="border-width: 0"
                src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a
            ><br />This work is licensed under a
            <a rel="license" href="http://creativecommons.org/licenses/by/4.0/"
              >Creative Commons Attribution 4.0 International License</a
            >.
          </template>
        </dd>
      </dl>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  async asyncData({ payload, context, app }) {
    if (payload) {
      return payload
    } else {
      const id = app.context.route.params.id
      const { data } = await axios.get(
        process.env.BASE_URL + `/data/curation.json`
      )
      const selections = data.selections
      for(let i = 0; i < selections.length; i++){
        const selection = selections[i]
        const manifest = selection.within["@id"]
        const members = selection.members
        for(let j = 0; j < members.length; j++){
          const member = members[j]
          const label = member["label"]
          if(label == id){
            member.manifest = manifest
            return member
          }
        }
      }
    }
  },

  data() {
    return {
      baseUrl: process.env.BASE_URL,
      fields : ["冊", "図", "区画南北", 
      "区画東西", "表a裏b", 
      "詳細区画", "朱z墨m", "図記号",
      "図説明", "水名", "水経注：巻",
      ]
    }
  },

  computed: {
    // 算出 getter 関数
    url() {
      // `this` は vm インスタンスを指します
      return this.baseUrl + '/item/' + this.$route.params.id
    },
    id() {
      return this.$route.params.id
    },
    title() {
      const metadata = this.metadata
      let title = this.label
      metadata.map((obj) => {
        if(obj.label == "地名/記述"){
          title = obj.value
        }
      })
      return title
    },
  },

  methods: {
    getIframeUrl() {
      const url =
        this.baseUrl +
        '/curation/?manifest=' +
        this.manifest +
        '&canvas=' +
        encodeURIComponent(this['@id'])
      return url
    },

    getCurationUrl() {
      const memberId = this['@id']
      const memberIdSpl = memberId.split('#xywh=')
      const canvasId = memberIdSpl[0]
      const xywh = memberIdSpl[1]
      const url =
        'http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=' +
        this.manifest +
        '&canvas=' +
        encodeURIComponent(canvasId) +
        '&xywh=' +
        xywh +
        '&xywh_highlight=border'
      return url
    }
  },

  head() {
    const title = this.title
    return {
      title,
      meta: [
        /*
        {
          hid: 'description',
          name: 'description',
          content: description,
        },
        */
        {
          hid: 'og:title',
          property: 'og:title',
          content: title,
        },
        {
          hid: 'og:type',
          property: 'og:type',
          content: 'article',
        },
        /*
        {
          hid: 'og:description',
          property: 'og:description',
          content: description,
        },
        */
        {
          hid: 'og:url',
          property: 'og:url',
          content: this.url,
        },
        {
          hid: 'og:image',
          property: 'og:image',
          content: this.thumbnail,
        },
        {
          hid: 'twitter:card',
          name: 'twitter:card',
          content: 'summary_large_image',
        },
      ],
    }
  },
}
</script>
