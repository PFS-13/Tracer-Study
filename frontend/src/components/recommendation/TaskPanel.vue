<template>
  <div id="mid-part">

    <el-card
      id="task-list-card"
      class="card"
    >

      <!-- HEADER -->
      <template #header>
        <div class="clearfix card-title">

          <img
            src="../../assets/task.png"
            class="card-logo"
          />

          <span>Task List</span>

        </div>
      </template>

      <!-- TASK LIST -->
      <div id="task-box">

        <div
          class="task-item"
          :id="'task-item-' + index"
          v-for="(item, index) in task_list"
          :key="item.task"
          @click="handleChooseTaskItem(item, index)"
        >

          <!-- TASK NAME -->
          <div
            class="task-item-name"
            :id="'task-item-name-' + index"
          >
            {{ item.task }}
          </div>

          <!-- TASK DESCRIPTION -->
          <div class="task-item-description">
            {{ item.description }}
          </div>

        </div>

      </div>

    </el-card>

  </div>
</template>

<script>
export default {
  name: 'TaskPanel',

  props: {

    task_list: {
      type: Array,
      default: () => []
    }

  },

  mounted() {
    console.log('TaskPanel mounted')
    console.log(this.task_list)
  },

  methods: {

    handleChooseTaskItem(item, index) {

      this.$emit(
        'chooseTaskItem',
        item,
        index
      )

    }

  }
}
</script>