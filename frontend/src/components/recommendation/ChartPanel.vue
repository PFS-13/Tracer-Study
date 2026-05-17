<template>
  <div id="right-part">

    <div id="right-setting-part">

      <div id="display-by-task-switch">
        <el-switch
          class="el-switch"
          :disabled="recommendation_mode !== '1'"
          :value="display_by_task"
          active-text="Display by task"
          @change="$emit('displayByTaskChange')"
        />
      </div>

      <div id="task_tag_box">
        <el-tag
          class="task-tag"
          v-for="item in chosen_task_items"
          :key="item"
        >
          {{ item }}
        </el-tag>
      </div>

    </div>

    <el-divider />

    <div id="chart-part">
      <!-- isi chart -->
    </div>

  </div>
</template>

<script>
export default {
  name: 'ChartPanel',

  props: {
    chosen_task_items: Array,
    recommendation_mode: String,
    display_by_task: Boolean,
    recommendation_chart: Object,
    has_recommendation: Boolean,
    ranking_scheme_radio: String,
    max_number_of_charts_after_recommendation: Number
  }
}
</script>