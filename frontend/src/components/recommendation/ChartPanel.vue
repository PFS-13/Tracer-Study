<template>
  <div id="right-part">

    <!-- TOP SETTING -->
    <div id="right-setting-part">

      <!-- DISPLAY BY TASK -->
      <div id="display-by-task-switch">

        <el-switch
          class="el-switch"
          :disabled="recommendation_mode !== '1'"
          :model-value="display_by_task"
          active-text="Display by task"
          @change="handleDisplayByTaskChange"
        >
        </el-switch>

      </div>

      <!-- TASK TAG -->
      <div id="task_tag_box">

        <el-tag
          class="task-tag"
          v-for="item in chosen_task_items"
          :key="item"
        >
          {{ transformFromTaskName(item) }}
        </el-tag>

      </div>

    </div>

    <el-divider></el-divider>

    <!-- EMPTY -->
    <div
      :key="1"
      v-if="!has_recommendation"
    >
    </div>

    <!-- CHART AREA -->
    <div
      id="chart-part"
      :key="2"
      v-else
    >

      <!-- INDIVIDUAL -->
      <div
        id="individual-recommendation-charts"
        v-if="recommendation_mode === '1'"
      >

        <!-- DISPLAY BY TASK -->
        <div
          id="individual-recommendation-display-by-task"
          v-if="display_by_task"
        >

          <div
            class="vega-chart-area-by-task"
            v-for="(item, index) in chosen_task_items"
            :key="index"
            v-show="recommendation_chart['Recos_nodedup'][item] !== undefined"
          >

            <!-- TITLE -->
            <el-tooltip
              content="Click to display more."
              placement="top"
              effect="light"
            >

              <div
                class="vega-chart-box-title"
                :id="generateId('vega-chart-box-title-', item)"
                @click="handleShowMoreChart(item)"
              >

                {{ transformFromTaskName(item) }}

                <img
                  class="vega-chart-box-title-logo"
                  :id="generateId('vega-chart-box-title-logo-', item)"
                  src="../../assets/close.png"
                />

                <div class="triangle-left"></div>

              </div>

            </el-tooltip>

            <!-- CHART BOX -->
            <div
              class="vega-chart-box-by-task"
              :id="generateId('vega-chart-box-by-', item)"
            >

              <div
                class="vega-chart"
                :id="generateId('vega-chart-' + item + '-', chart_index)"
                v-for="(chart_item, chart_index)
                in recommendation_chart['Recos_nodedup'][item]['R1']"
                :key="chart_index"
                @click="handleShowChartDialog(item, chart_index)"
              >
              </div>

            </div>

          </div>

        </div>

        <!-- DISPLAY NOT BY TASK -->
        <div
          id="individual-recommendation-display-not-by-task"
          v-if="!display_by_task"
        >

          <div class="vega-chart-box">

            <div
              class="vega-chart-with-task-title"
              v-for="(chart_item, chart_index)
              in recommendation_chart['Recos_dedup']['R1']"
              :key="chart_index"
              v-show="chart_index < max_number_of_charts_after_recommendation"
            >

              <!-- R1 -->
              <div
                class="vega-chart-task-title"
                v-if="ranking_scheme_radio === '1'"
              >

                <el-tag
                  class="vega-chart-task-title-tag"
                  v-for="(tag_item, tag_index)
                  in recommendation_chart['Recos_dedup']['R1'][chart_index]['task']"
                  :key="tag_index"
                  size="small"
                >
                  {{ tag_item }}
                </el-tag>

              </div>

              <!-- R2 -->
              <div
                class="vega-chart-task-title"
                v-if="ranking_scheme_radio === '2'"
              >

                <el-tag
                  class="vega-chart-task-title-tag"
                  v-for="(tag_item, tag_index)
                  in recommendation_chart['Recos_dedup']['R2'][chart_index]['task']"
                  :key="tag_index"
                  size="small"
                >
                  {{ tag_item }}
                </el-tag>

              </div>

              <!-- R3 -->
              <div
                class="vega-chart-task-title"
                v-if="ranking_scheme_radio === '3'"
              >

                <el-tag
                  class="vega-chart-task-title-tag"
                  v-for="(tag_item, tag_index)
                  in recommendation_chart['Recos_dedup']['R3'][chart_index]['task']"
                  :key="tag_index"
                  size="small"
                >
                  {{ tag_item }}
                </el-tag>

              </div>

              <!-- R4 -->
              <div
                class="vega-chart-task-title"
                v-if="ranking_scheme_radio === '4'"
              >

                <el-tag
                  class="vega-chart-task-title-tag"
                  v-for="(tag_item, tag_index)
                  in recommendation_chart['Recos_dedup']['R4'][chart_index]['task']"
                  :key="tag_index"
                  size="small"
                >
                  {{ tag_item }}
                </el-tag>

              </div>

              <!-- VEGA -->
              <div
                class="vega-chart"
                :id="generateId('vega-chart-', chart_index)"
                @click="handleShowChartDialog(null, chart_index)"
              >
              </div>

            </div>

          </div>

        </div>

      </div>

      <!-- COMBINATION -->
      <div
        id="combination-recommendation-charts"
        v-if="recommendation_mode === '2'"
      >

        <div
          class="vega-chart"
          :id="generateId('vega-chart-', index)"
          v-for="(item, index) in recommendation_chart"
          :key="index"
          @click="handleShowChartDialog(null, index)"
        >
        </div>

        <div id="vega-chart-test"></div>

      </div>

    </div>

  </div>
</template>

<script>
export default {
  name: 'ChartPanel',

  props: {

    chosen_task_items: {
      type: Array,
      default: () => []
    },

    recommendation_mode: {
      type: String,
      default: '1'
    },

    display_by_task: {
      type: Boolean,
      default: true
    },

    recommendation_chart: {
      type: Object,
      default: () => ({})
    },

    has_recommendation: {
      type: Boolean,
      default: false
    },

    ranking_scheme_radio: {
      type: String,
      default: '1'
    },

    max_number_of_charts_after_recommendation: {
      type: Number,
      default: 10
    }

  },

  methods: {

    handleDisplayByTaskChange() {

      this.$emit(
        'displayByTaskChange'
      )

    },

    handleShowChartDialog(task, index) {

      this.$emit(
        'showChartDialog',
        task,
        index
      )

    },

    handleShowMoreChart(task) {

      this.$emit(
        'showMoreChart',
        task
      )

    },

    generateId(baseId, index) {

      return baseId + index

    },

    transformFromTaskName(transTaskName) {

      let s = transTaskName.replace(/_/g, ' ')

      let ss = s.toLowerCase().split(/\s+/)

      for (let i = 0; i < ss.length; i++) {

        ss[i] =
          ss[i].slice(0, 1).toUpperCase() +
          ss[i].slice(1)

      }

      return ss.join(' ')

    }

  }
}
</script>