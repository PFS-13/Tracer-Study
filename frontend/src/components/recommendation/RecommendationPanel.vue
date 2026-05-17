<script setup lang="ts">

defineProps([
  'recommendation_mode',
  'display_by_task',
  'chosen_task_items',
  'recommendation_chart',
  'ranking_scheme_radio',
  'max_number_of_charts_after_recommendation',
  'has_recommendation',
  'generate_id',
  'show_more_chart',
  'show_chart_dialog',
  'transform_from_task_name',
  'display_by_task_change'
])

</script>

<template>

<div id="right-part">

  <div id="right-setting-part">

    <div id="display-by-task-switch">

      <el-switch
        class="el-switch"
        :disabled="recommendation_mode !== '1'"
        v-model="display_by_task"
        active-text="Display by task"
        @change="display_by_task_change()"
      />

    </div>

    <div id="task_tag_box">

      <el-tag
        class="task-tag"
        v-for="item in chosen_task_items"
        :key="item"
      >
        {{ transform_from_task_name(item) }}
      </el-tag>

    </div>

  </div>

  <el-divider />

  <div :key="1" v-if="!has_recommendation"></div>

  <div id="chart-part" :key="2" v-else>

    <div
      id="individual-recommendation-charts"
      v-if="recommendation_mode==='1'"
    >

      <div
        id="individual-recommendation-display-by-task"
        v-if="display_by_task"
      >

        <div
          class="vega-chart-area-by-task"
          v-for="(item, index) in chosen_task_items"
          v-if="recommendation_chart['Recos_nodedup'][item] !== undefined"
          :key="index"
        >

          <el-tooltip
            content="Click to display more."
            placement="top"
            effect="light"
          >

            <div
              class="vega-chart-box-title"
              :id="generate_id('vega-chart-box-title-', item)"
              @click="show_more_chart(item)"
            >

              {{ transform_from_task_name(item) }}

              <img
                class="vega-chart-box-title-logo"
                :id="generate_id('vega-chart-box-title-logo-', item)"
                src="@/assets/close.png"
              />

              <div class="triangle-left"></div>

            </div>

          </el-tooltip>

          <div
            class="vega-chart-box-by-task"
            :id="generate_id('vega-chart-box-by-', item)"
          >

            <div
              class="vega-chart"
              :id="generate_id('vega-chart-' + item + '-', chart_index)"
              v-for="(chart_item, chart_index)
              in recommendation_chart['Recos_nodedup'][item]['R1']"
              :key="chart_index"
              @click="show_chart_dialog(item, chart_index)"
            ></div>

          </div>

        </div>

      </div>

      <div
        id="individual-recommendation-display-not-by-task"
        v-if="!display_by_task"
      >

        <div class="vega-chart-box">

          <div
            class="vega-chart-with-task-title"
            v-for="(chart_item, chart_index)
            in recommendation_chart['Recos_dedup']['R1']"
            v-if="chart_index < max_number_of_charts_after_recommendation"
            :key="chart_index"
          >

            <div
              class="vega-chart-task-title"
              v-if="ranking_scheme_radio==='1'"
            >

              <el-tag
                class="vega-chart-task-title-tag"
                v-for="(tag_item, tag_index)
                in recommendation_chart['Recos_dedup']['R1'][chart_index]['task']"
                :key="tag_index"
                size="mini"
              >
                {{ tag_item }}
              </el-tag>

            </div>

            <div
              class="vega-chart"
              :id="generate_id('vega-chart-', chart_index)"
              @click="show_chart_dialog(null, chart_index)"
            ></div>

          </div>

        </div>

      </div>

    </div>

    <div
      id="combination-recommendation-charts"
      v-if="recommendation_mode==='2'"
    >

      <div
        class="vega-chart"
        :id="generate_id('vega-chart-', index)"
        v-for="(item, index) in recommendation_chart"
        :key="index"
        @click="show_chart_dialog(null, index)"
      ></div>

      <div id="vega-chart-test"></div>

    </div>

  </div>

</div>

</template>