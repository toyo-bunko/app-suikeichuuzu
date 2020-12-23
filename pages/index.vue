<template>
  <div>
    <section class="mb-5">
      <v-parallax :src="baseUrl + '/img/ogp/home.jpg'" height="300">
        <v-layout column align-center justify-center class="white--text">
          <h1 class="white--text mb-2 display-1 text-center">
            <b>{{title}}</b>
          </h1>
          <v-btn
            large
            class="mt-5"
            :to="localePath({ name: 'search' })"
            color="primary"
            >{{ $t('try_out') }}</v-btn
          >
        </v-layout>
      </v-parallax>
    </section>

    <v-container>
      <v-card class="my-5">
        <v-card-title>
          <h2>{{ $t('about_') }}</h2>
        </v-card-title>
        <v-card-text>
          <div class="text--primary">
              <p>
                水系注図DBへようこそ！
              </p>
          </div>
        </v-card-text>
      </v-card>

      <v-card class="my-5">
        <v-card-title>
          <h2>{{ $t('members') }}</h2>
        </v-card-title>
        <v-card-text>
          <div class="text--primary">
            <ul>
                <li>
                  <a href="http://www.toyo-bunko.or.jp/">東洋文庫</a
                  >
                </li>
                <li>
                  <a href="https://researchmap.jp/nakamura.satoru/">中村覚</a>,
                  東京大学 史料編纂所 助教
                </li>
            </ul>
          </div>
        </v-card-text>
      </v-card>

      <v-card class="my-5">
        <v-card-title>
          <h2>{{ $t('updates') }}</h2>
        </v-card-title>
        <v-card-text>
            <div class="text--primary">
              <ul>
                <li>
                  23, Dec., 2020: prototyping.
                </li>
              </ul>
            </div>
        </v-card-text>
      </v-card>
      <v-card class="my-5">
        <v-card-title>
          <h2>{{ $t('contact_information') }}</h2>
        </v-card-title>
        <v-card-text>
          <div class="text--primary">
            東洋文庫
            :
            <a href="http://www.toyo-bunko.or.jp/"
              >http://www.toyo-bunko.or.jp/</a
            >
          </div>
        </v-card-text>
      </v-card>

      <br />
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      baseUrl: process.env.BASE_URL,
      title : '水系注図DB'
    }
  },
  head() {
    const title = this.title
    return {
      titleTemplate: null,
      title,
    }
  },
}
</script>
