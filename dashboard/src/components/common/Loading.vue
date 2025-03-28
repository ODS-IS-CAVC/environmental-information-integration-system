<script lang="ts" setup>
/**
 * Loading.vue
 * 共通ローディングコンポーネント
 * 
 * 親コンポーネント
 * @/views/Watch.vue
 */
</script>
<template>
  <div class="loading">
    <div class="loading__spacer">
      <v-progress-circular
        :size="70"
        :width="10"
        color="purple"
        indeterminate
      />
    </div>
  </div>
</template>
<style scoped>
  .loading {
    z-index: 9999;
    width: 100%;
    height: 100%;
    background: #fefefe;
    background-color: rgba(0, 0, 0, 0.3);
    position: fixed;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .loading__spacer {
    height: 10%;
  }
</style>
