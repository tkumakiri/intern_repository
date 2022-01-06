<template>
  <v-app>
    <v-container>
      <v-list>
        <v-list-item>
          <v-list-item-title class="text-h6"
            >00月00日開催 ライブ</v-list-item-title
          >
          <v-list-item-icon>
            <v-btn fab dark color="indigo">
              <v-icon dark> mdi-plus </v-icon>
            </v-btn>
          </v-list-item-icon>
        </v-list-item>
      </v-list>
      <!-- v-forで行う -->
      <v-card class="mb-2">
        <v-list>
          <v-list-item>
            <v-list-item-avatar>
              <v-img src="../assets/testuser.png" max-width="100" />
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="text-h6">ユーザー１</v-list-item-title>
              <div>まぢぱない</div>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card>

      <v-card>
        <v-list>
          <v-list-item>
            <v-list-item-avatar>
              <v-img src="../assets/testuser.png" max-width="100" />
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="text-h6">ユーザー１</v-list-item-title>
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
    </v-container>
  </v-app>
</template>

<script>
export default {
  name: "LiveDetail",
};
</script>

<style scoped></style>
