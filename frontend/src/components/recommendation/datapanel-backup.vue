<template>
  <div id="left-part">

    <el-card id="data-card" class="card">

      <template #header>
        <div class="clearfix card-title">
          <img src="../../assets/database.png" class="card-logo" />
          <span>Data</span>
        </div>
      </template>

      <el-select
        :model-value="dataset_value"
        placeholder="Choosing a Dataset"
        @change="$emit('chooseDataset', $event)"
      >
        <el-option
          v-for="item in dataset_options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>

      <!-- multi select column -->
      <div class="data-list">
        <div
          v-for="column in data_list"
          :key="column.field"
          class="data-item"
          :class="{ active: isSelected(column) }"
          @click="toggleColumn(column)"
        >
          <el-checkbox
            :model-value="isSelected(column)"
            @change="toggleColumn(column)"
            @click.stop
          >
            {{ column.field }}
          </el-checkbox>
        </div>
      </div>

    </el-card>

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
    dataset_options: Array,
    dataset_value: String,
    data_list: Array,
    data_type: Object
  },

  data() {
    return {
      selected_columns: []
    }
  },

  methods: {

    isSelected(column) {
      return this.selected_columns.some(
        item => item.field === column.field
      )
    },

    toggleColumn(column) {

      const index = this.selected_columns.findIndex(
        item => item.field === column.field
      )

      // jika sudah ada -> hapus
      if (index !== -1) {
        this.selected_columns.splice(index, 1)
      }

      // jika belum ada -> tambah
      else {
        this.selected_columns.push(column)
      }

      console.log(this.selected_columns)

      // kirim ke parent
      this.$emit("chooseColumn", this.selected_columns)
    },recommendation () {
        let requestData = {}
        requestData['ColumnTypes'] = this.chosen_data_items
        requestData['task'] = this.chosen_task_items
        requestData['dataset'] = this.dataset_value
        requestData['mode'] = (this.recommendation_mode_radio === '1') ? 2 : 5
        this.recommendation_mode = this.recommendation_mode_radio
        this.max_number_of_charts_after_recommendation = this.max_number_of_charts
        this.$axios.post('api/Reco', requestData)
          .then(Response => {
            console.log(Response.data)
            this.has_recommendation = true
            this.recommendation_chart = Response.data['Recos']
            this.recommendation_data = Response.data['Data']
            this.paint_chart()
          })
      },
      paint_chart () {
        // TODO 绘制图表
        if (this.recommendation_mode_radio === '1') {
          if (this.display_by_task) {
            for (let i = 0; i < this.chosen_task_items.length; i++) {
              let task = this.chosen_task_items[i]
              if (this.recommendation_chart['Recos_nodedup'][task] === undefined) continue
              let R = {}
              switch (this.ranking_scheme_radio) {
                case '1':
                  R = this.recommendation_chart['Recos_nodedup'][task]['R1']
                  break
                case '2':
                  R = this.recommendation_chart['Recos_nodedup'][task]['R2']
                  break
                case '3':
                  R = this.recommendation_chart['Recos_nodedup'][task]['R3']
                  break
                case '4':
                  R = this.recommendation_chart['Recos_nodedup'][task]['R4']
                  break
              }
              for (let j = 0; j < R.length && j < this.max_number_of_charts; j++) {
                let props = this.set_chart_config(R[j]['props'])
                embed('#vega-chart-' + task + '-' + j, props).then(function (result) {}).catch(console.error)
              }
            }
          } else {
            let R = {}
            switch (this.ranking_scheme_radio) {
              case '1':
                R = this.recommendation_chart['Recos_dedup']['R1']
                break
              case '2':
                R = this.recommendation_chart['Recos_dedup']['R2']
                break
              case '3':
                R = this.recommendation_chart['Recos_dedup']['R3']
                break
              case '4':
                R = this.recommendation_chart['Recos_dedup']['R4']
                break
            }
            for (let j = 0; j < R.length && j < this.max_number_of_charts; j++) {
              let props = this.set_chart_config(R[j]['props'])
              embed('#vega-chart-' + j, props).then(function (result) {}).catch(console.error)
            }
          }
        } else if (this.recommendation_mode_radio === '2') {
          for (let i = 0; i < this.recommendation_chart.length && i < this.max_number_of_charts; i++) {
            let props = this.set_chart_config(this.recommendation_chart[i]['props'])
            embed('#vega-chart-' + i, props).then(function (result) {}).catch(console.error)
          }
        }
      },
  }
}
</script>

<style scoped>

.data-list {
  margin-top: 15px;
}

.data-item {
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: 0.2s;
  border: 1px solid #dcdfe6;
}

.data-item:hover {
  background: #f5f7fa;
}

/* item terpilih */
.data-item.active {
  background: #ecf5ff;
  border: 1px solid #409eff;
}

</style>