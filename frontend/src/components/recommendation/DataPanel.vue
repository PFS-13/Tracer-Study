<template>
  <div id="left-part">

    <!-- DATA CARD -->
    <el-card id="data-card" class="card">

      <template #header>
        <div class="clearfix card-title">
          <img
            src="../../assets/database.png"
            class="card-logo"
          />
          <span>Data</span>
        </div>
      </template>

      <!-- DATASET SELECT -->
      <el-select
        :model-value="dataset_value"
        placeholder="Choosing a Dataset"
        style="width: 100%"
        @change="handleDatasetChange"
      >

        <el-option
          v-for="item in dataset_options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>

      </el-select>

      <el-divider></el-divider>

      <!-- DATA COLUMN LIST -->
      <div id="data-box">

        <div
          class="data-item"
          :id="'data-item-' + index"
          v-for="(item, index) in data_list"
          :key="item.field"
          @click="handleChooseDataItem(item, index)"
        >

          <div
            class="data-item-icon"
            :id="'data-item-icon-' + index"
          >
            {{ data_type[item.type] }}
          </div>

          <div class="data-item-text">

            <div
              class="data-item-field"
              :id="'data-item-field-' + index"
            >
              {{ item.field }}
            </div>

            <div class="data-item-type">
              {{ item.type }}
            </div>

          </div>

        </div>

      </div>

    </el-card>

    <!-- SETTING CARD -->
    <el-card id="setting-card" class="card">

      <template #header>
        <div class="clearfix card-title">
          <img
            src="../../assets/setting.png"
            class="card-logo"
          />
          <span>Setting</span>
        </div>
      </template>

      <!-- MAX NUMBER -->
      <div id="max-number-of-charts">

        <div class="setting-title">
          Max Number of Charts
        </div>

        <el-input-number
          id="max-number-of-charts-input"
          :model-value="max_number_of_charts"
          size="small"
          :min="1"
          @change="handleMaxChartChange"
        >
        </el-input-number>

      </div>

      <el-divider></el-divider>

      <!-- RECOMMENDATION MODE -->
      <div id="recommendation-mode">

        <div class="setting-title">
          Recommendation Mode
        </div>

        <el-radio-group
          :model-value="recommendation_mode_radio"
          @change="handleRecommendationModeChange"
        >

          <el-radio value="1">
            Individual Recommendation
          </el-radio>

          <el-radio value="2">
            Combination Recommendation
          </el-radio>

        </el-radio-group>

      </div>

      <el-divider></el-divider>

      <!-- RANKING -->
      <div id="ranking-scheme">

        <div class="setting-title">
          Ranking Scheme
        </div>

        <el-radio-group
          :model-value="ranking_scheme_radio"
          @change="handleRankingChange"
        >

          <el-radio value="1">
            Complexity-based ranking
          </el-radio>

          <el-radio value="2">
            Reverse-complexity-based ranking
          </el-radio>

          <el-radio value="3">
            Interested-data-columns-based ranking
          </el-radio>

          <el-radio value="4">
            Tasks-coverage-based ranking
          </el-radio>

        </el-radio-group>

      </div>

    </el-card>

    <!-- BUTTON -->
    <el-button
      id="recommendation-button"
      type="primary"
      @click="$emit('recommendation')"
    >
      Recommendation
    </el-button>

  </div>
</template>

<script>
export default {
  name: 'DataPanel',

  props: {
    dataset_options: {
      type: Array,
      default: () => []
    },

    dataset_value: {
      type: String,
      default: ''
    },

    data_list: {
      type: Array,
      default: () => []
    },

    data_type: {
      type: Object,
      default: () => ({})
    },

    max_number_of_charts: {
      type: Number,
      default: 10
    },

    recommendation_mode_radio: {
      type: String,
      default: '1'
    },

    ranking_scheme_radio: {
      type: String,
      default: '1'
    }
  },

  mounted() {
    console.log('DataPanel mounted')
    console.log(this.dataset_options)
  },

  methods: {

    handleDatasetChange(value) {
      this.$emit('chooseDataset', value)
    },

    handleChooseDataItem(item, index) {
      this.$emit('chooseDataItem', item, index)
    },

    handleMaxChartChange(value) {
      this.$emit('updateMaxChart', value)
    },

    handleRecommendationModeChange(value) {
      this.$emit('updateRecommendationMode', value)
    },

    handleRankingChange(value) {
      this.$emit('updateRankingScheme', value)
    }

  }
}
</script>