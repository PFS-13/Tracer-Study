<script setup lang="ts">

import DataPanel from '@/components/data/DataPanel.vue'
import SettingPanel from '@/components/setting/SettingPanel.vue'
import TaskList from '@/components/task/TaskList.vue'
// import RecommendationPanel from '@/components/recommendation/RecommendationPanel.vue'

</script>

<template>

  <div class="page">

    <DataPanel />

    <SettingPanel />

    <TaskList />

    <RecommendationPanel />

  </div>

</template>