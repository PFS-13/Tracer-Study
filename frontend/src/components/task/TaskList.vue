<script setup lang="ts">

import { ref } from 'vue'

interface TaskItem {
  task: string
  description: string
}


/* =========================
   STATE
========================= */

const taskList = ref<TaskItem[]>([
  {
    task: 'Distribution',
    description: 'Analyze data distribution'
  },
  {
    task: 'Comparison',
    description: 'Compare categories'
  },
  {
    task: 'Trend',
    description: 'Analyze temporal trend'
  },
  {
    task: 'Correlation',
    description: 'Analyze relationship between variables'
  }
])


/* =========================
   METHODS
========================= */

const chooseTaskItem = (
  item: TaskItem,
  index: number
) => {

  console.log('Task Selected:')

  console.log(item)

}

const generateId = (
  prefix: string,
  index: number
) => {

  return `${prefix}${index}`

}

</script>

<template>

  <el-card
    id="task-list-card"
    class="card"
  >

    <template #header>

      <div class="clearfix card-title">

        <img
          src="@/assets/task.png"
          class="card-logo"
        />

        <span>Task List</span>

      </div>

    </template>

    <div id="task-box">

      <div
        class="task-item"
        :id="generateId('task-item-', index)"
        v-for="(item, index) in taskList"
        :key="item.task"
        @click="chooseTaskItem(item, index)"
      >

        <div
          class="task-item-name"
          :id="generateId('task-item-name-', index)"
        >
          {{ item.task }}
        </div>

        <div
          class="task-item-description"
          :id="generateId('task-item-description-', index)"
        >
          {{ item.description }}
        </div>

      </div>

    </div>

  </el-card>

</template>