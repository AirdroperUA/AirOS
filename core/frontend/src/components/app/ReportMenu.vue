<template>
  <v-container
    id="feature-request-button"
    class="d-flex justify-center"
  >
    <v-btn
      class="mr-2"
      icon
      large
      elevation="2"
      @click="showDialog(true)"
    >
      <v-icon>mdi-bug</v-icon>
    </v-btn>
    <v-dialog
      width="fit-content"
      :value="show_dialog"
      @input="showDialog"
    >
      <v-card>
        <v-card-title class="align-center">
          Bug report / Feature request
        </v-card-title>

        <v-divider />

        <v-container class="pa-2">
          <v-card-actions class="flex-column">
            <v-btn
              v-tooltip="'Track changes, contribute, and get notified when fixed'"
              class="ma-2"
              @click="openGitHub()"
            >
              <v-icon
                left
                size="20"
              >
                mdi-github
              </v-icon>
              With GitHub
            </v-btn>
          </v-card-actions>
        </v-container>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import * as Sentry from '@sentry/vue'
import Vue from 'vue'

export default Vue.extend({
  name: 'ReportMenu',
  data() {
    return {
      show_dialog: false,
    }
  },
  methods: {
    showDialog(state: boolean): void {
      this.show_dialog = state
    },
    openGitHub(): void {
      window.open('https://github.com/AirdroperUA/bug_report/issues/new', '_blank')
    }
  },
})
</script>
