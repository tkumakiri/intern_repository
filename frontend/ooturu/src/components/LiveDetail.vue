<template>
  <v-app class="blue-grey lighten-5">
    <v-row justify="center">
      <v-card width="1000" height="auto">
        <v-list>
          <v-list-item>
            <h1>00月00日開催 ライブ</h1>
            <v-list-item-icon>
              <v-btn fab dark color="indigo" @click="onClickTweet">
                <v-icon dark> mdi-plus </v-icon>
              </v-btn>
            </v-list-item-icon>
          </v-list-item>
        </v-list>
        <v-row justify="center">
          <!-- v-forで行う -->
          <v-card width="800" class="mb-2">
            <v-list>
              <v-list-item>
                <v-list-item-avatar @click="onClickUser">
                  <v-img src="../assets/testuser.png" max-width="100" />
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title class="text-h6"
                    >ユーザー１</v-list-item-title
                  >
                  <div>まぢぱない</div>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>

          <v-card width="800">
            <v-list>
              <v-list-item>
                <v-list-item-avatar>
                  <v-img src="../assets/testuser.png" max-width="100" />
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title class="text-h6"
                    >ユーザー１</v-list-item-title
                  >
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <div>まぢぱない</div>
              </v-list-item>
              <v-list-item>
                <v-img src="../assets/testphoto.jpeg"></v-img>
              </v-list-item>
              <v-list-item>
                <v-list-item-icon class="ml-auto">
                  <v-btn class="mx-2" fab dark small color="pink">
                    <v-icon dark> mdi-heart </v-icon>
                  </v-btn>
                </v-list-item-icon>
              </v-list-item>
            </v-list>
          </v-card>
        </v-row>
      </v-card>
    </v-row>
  </v-app>
</template>

<script>
export default {
  name: "LiveDetail",
  methods: {
    onClickUser: function () {
      this.$router.push("/userprofile");
    },
    onClickTweet: function () {
      this.$router.push("/tweet");
    },
  },
};
</script>

<style scoped></style>
