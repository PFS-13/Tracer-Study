<template>
  <div id="page">
    <div id="title-bar">
      <div id="title">
        <b>Visual Data Analysis with Task-based Recommendations</b>
      </div>
    </div>

    <div id="main-part">

      <DataPanel
        :dataset_options="dataset_options"
        :dataset_value="dataset_value"
        :data_list="data_list"
        :data_type="data_type"
        :max_number_of_charts="max_number_of_charts"
        :recommendation_mode_radio="recommendation_mode_radio"
        :ranking_scheme_radio="ranking_scheme_radio"
        @chooseDataset="choose_dataset"
        @chooseDataItem="choose_data_item"
        @recommendation="recommendation"
      />

      <TaskPanel
        :task_list="task_list"
        @chooseTaskItem="choose_task_item"
      />

      <ChartPanel
        :chosen_task_items="chosen_task_items"
        :recommendation_mode="recommendation_mode"
        :display_by_task="display_by_task"
        :recommendation_chart="recommendation_chart"
        :has_recommendation="has_recommendation"
        :ranking_scheme_radio="ranking_scheme_radio"
        :max_number_of_charts_after_recommendation="max_number_of_charts_after_recommendation"
        @displayByTaskChange="display_by_task_change"
        @showChartDialog="show_chart_dialog"
        @showMoreChart="show_more_chart"
      />

    </div>
  </div>
</template>

<script>
import embed from 'vega-embed'

import DataPanel from './components/recommendation/DataPanel.vue'
import TaskPanel from './components/recommendation/TaskPanel.vue'
import ChartPanel from './components/recommendation/ChartPanel.vue'

import './assets/styles/main.css'

export default {
  name: 'App',

  components: {
    DataPanel,
    TaskPanel,
    ChartPanel
  },

  data () {
    return {
        dataset_options: [{
          value: 'mahasiswa',
          label: 'Mahasiswa'
        }],
        data_type: {
          'temporal': 'T',
          'quantitative': 'Q',
          'nominal': 'N',
          'ordinal': 'O'
        },
        task_list: [
          {
            task: 'Change Over Time',
            description: 'Analyse how the data changes over time series.'
          },{
            task: 'Comparison',
            description: 'Give emphasis to comparison on different entities.'
          }, {
            task: 'Compute Derived Value',
            description: 'Compute aggregated or binned numeric derived value.'
          }, {
            task: 'Part to Whole',
            description: 'Show component elements of a single entity.'
          }
        ],
        dataset_value: '',
        max_number_of_charts: 10,
        max_number_of_charts_after_recommendation: 10, // 按下推荐按钮后确定的数值
        recommendation_mode_radio: '1',
        recommendation_mode: '0', // 按下推荐按钮后确定的数值
        ranking_scheme_radio: '1',
        data_list: [],
        chosen_data_items: [],
        chosen_task_items: [],
        task_checked: [false, false, false, false, false, false, false, false,
          false, false, false, false, false, false, false, false, false],
        display_by_task: true,
        recommendation_chart: {
          'Recos_dedup': {'R1': [], 'R2': [], 'R3': [], 'R4': []},
          'Recos_nodedup': {'R1': [], 'R2': [], 'R3': [], 'R4': []}
        },
        recommendation_data: [],
        has_recommendation: false,
        chart_dialog_visible: false
      }
  },

  methods: {
      choose_dataset (dataset) {
        this.dataset_value = dataset
        this.$axios.get('api/columns?dataset=' + dataset)
        .then(response => {
          this.data_list = response.data
          console.log("data list :", this.data_list)
        })
      },
      recommendation () {
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
      choose_data_item (item, index) {
        // TODO 选中数据种类
        let icon = document.getElementById('data-item-icon-' + index)
        let field = document.getElementById('data-item-field-' + index)
        for (let i = 0; i < this.chosen_data_items.length; i++) {
          if (this.chosen_data_items[i].field === item.field) {
            // 已选中，现在撤销选中
            this.chosen_data_items.splice(i, 1)
            icon.style['background'] = 'darkgrey'
            field.style['color'] = 'black'
            // console.log(this.chosen_data_items)
            return
          }
        }
        // 没选中，选中对象
        this.chosen_data_items.push(item)
        icon.style.background = 'dodgerblue'
        field.style['color'] = 'dodgerblue'
        // console.log(this.chosen_data_items)
      },
      choose_task_item (item, index) {
        let taskItem = document.getElementById('task-item-' + index)
        let name = document.getElementById('task-item-name-' + index)
        for (let i = 0; i < this.chosen_task_items.length; i++) {
          if (this.chosen_task_items[i] === this.transform_task_name(item.task)) {
            // 已选中，现在撤销选中
            this.chosen_task_items.splice(i, 1)
            name.style['color'] = 'black'
            taskItem.style['border-left-width'] = '0'
            console.log(this.chosen_task_items)
            return
          }
        }
        // 没选中，选中对象
        this.chosen_task_items.push(this.transform_task_name(item.task))
        name.style['color'] = 'dodgerblue'
        taskItem.style['border-left-width'] = '4px'
        console.log(this.chosen_task_items)
      },
      display_by_task_change () {
        this.paint_chart()
      },
      show_chart_dialog (task, index) {
        this.chart_dialog_visible = true
        let props = {}
        if (this.recommendation_mode_radio === '1') {
          let R = 'R1'
          switch (this.ranking_scheme_radio) {
            case '1':
              R = 'R1'
              break
            case '2':
              R = 'R2'
              break
            case '3':
              R = 'R3'
              break
            case '4':
              R = 'R4'
              break
          }
          if (this.display_by_task) {
            props = this.set_dialog_chart_config(this.recommendation_chart['Recos_nodedup'][task][R][index]['props'])
          } else {
            props = this.set_dialog_chart_config(this.recommendation_chart['Recos_dedup'][R][index]['props'])
          }
        } else {
          props = this.set_dialog_chart_config(this.recommendation_chart[index]['props'])
        }
        console.log(props)
        embed('#dialog-chart', props)
          .then(function (result) {
          }).catch(console.error)
      },
      set_chart_config (props) {
        props['data'] = {'name': 'table', 'values': this.recommendation_data}
        props['height'] = 200
        props['width'] = 200
        if (props['encoding'] === undefined) {
          props['encoding'] = {}
        }
        if (props['encoding']['x'] === undefined) {
          props['encoding']['x'] = {}
        }
        if (props['encoding']['x']['axis'] === undefined) {
          props['encoding']['x']['axis'] = {}
        }
        props['encoding']['x']['axis']['labelAngle'] = -45
        console.log("haha", props)
        return props
      },
      set_dialog_chart_config (props) {
        props['height'] = 600
        props['width'] = 1400
        // delete props['height']
        // delete props['width']
        return props
      },
      show_more_chart (task) {
        let box = document.getElementById('vega-chart-box-by-' + task)
        let title = document.getElementById('vega-chart-box-title-' + task)
        // let logo = document.getElementById('vega-chart-box-title-logo-' + task)
        if (box.style['height'] === 'auto') {
          title.style['width'] = 'fit-content'
          box.style['height'] = '300px'
        } else {
          title.style['width'] = '500px'
          box.style['height'] = 'auto'
        }
        return false
      },
      ranking_change () {
        this.paint_chart()
      },
      generate_id (baseId, index) {
        return baseId + index
      },
      transform_task_name (taskName) {
        return taskName.toLowerCase().replace(/ /g, '_')
      },
      transform_from_task_name (transTaskName) {
        let s = transTaskName.replace(/_/g, ' ')
        let ss = s.toLowerCase().split(/\s+/)
        for (let i = 0; i < ss.length; i++) {
          ss[i] = ss[i].slice(0, 1).toUpperCase() + ss[i].slice(1)
        }
        return ss.join(' ')
      }
    }
}
</script>