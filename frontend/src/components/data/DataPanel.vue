<script setup lang="ts">

import { ref } from 'vue'

interface DatasetOption {
  label: string
  value: string
}

interface DataItem {
  field: string
  type: string
}


/* =========================
   STATE
========================= */

const datasetValue = ref('')

const datasetOptions = ref<DatasetOption[]>([
  {
    label: 'Tracer Study',
    value: 'tracer'
  },
  {
    label: 'Graduate Survey',
    value: 'graduate'
  }
])

const dataList = ref<DataItem[]>([
  {
    field: 'Salary',
    type: 'quantitative'
  },
  {
    field: 'Gender',
    type: 'nominal'
  },
  {
    field: 'Study Program',
    type: 'nominal'
  }
])

const dataType: Record<string, string> = {
  quantitative: 'Q',
  nominal: 'N',
  ordinal: 'O',
  temporal: 'T'
}



const chooseDataset = (
  value: string
) => {

  datasetValue.value = value

  console.log('Dataset:', value)

}

const chooseDataItem = (
  item: DataItem,
  index: number
) => {

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
    id="data-card"
    class="card"
  >

    <template #header>

      <div class="clearfix card-title">

        <img
          src="@/assets/database.png"
          class="card-logo"
        />

        <span>Data</span>

      </div>

    </template>

    <el-select
      v-model="datasetValue"
      placeholder="Choosing a Dataset"
      @change="chooseDataset"
    >

      <el-option
        v-for="item in datasetOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />

    </el-select>

    <el-divider />

    <div id="data-box">

      <div
        class="data-item"
        :id="generateId('data-item-', index)"
        v-for="(item, index) in dataList"
        :key="item.field"
        @click="chooseDataItem(item, index)"
      >

        <div
          class="data-item-icon"
          :id="generateId('data-item-icon-', index)"
        >
          {{ dataType[item.type] }}
        </div>

        <div class="data-item-text">

          <div
            class="data-item-field"
            :id="generateId('data-item-field-', index)"
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

</template>