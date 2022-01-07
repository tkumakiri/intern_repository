<template>
  <v-app class="blue-grey lighten-5">
    <v-row justify="center">
      <v-list width="500" class="mt-5">
        <v-list-item>
          <v-list-item-avatar>
            <v-img src="../assets/testuser.png" max-width="100" />
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title class="text-h6">ユーザー１</v-list-item-title>
            <div>まぢぱない</div>
          </v-list-item-content>
        </v-list-item>

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
    </v-row>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field
        label="Say your thoughts!"
        v-model.trim="tweet"
        :counter="255"
        :rules="tweetRules"
        required
        solo
      >
      </v-text-field>
      <v-spacer />
      <v-btn color="primary mr-4" @click="storeTweet" :disabled="!canSubmit"
        >Tweet!</v-btn
      >
    </v-form>
  </v-app>
</template>

<script>
export default {};
</script>

<style scoped></style>
