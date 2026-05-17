<script setup lang="ts">

import { ref } from 'vue'
import api from '../../services/api'

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
  }
])

const dataList = ref<DataItem[]>([])


const dataType: Record<string, string> = {
  quantitative: 'Q',
  nominal: 'N',
  ordinal: 'O',
  temporal: 'T'
}



const chooseDataset = async (
  value: string
) => {

  datasetValue.value = value

  console.log('select dataset ' + value)

  try {

    const response = await api.get(
      '/api/columns',
      {
        params: {
          dataset: value
        }
      }
    )

    if (
      typeof response.data[0]?.length
      === 'number'
    ) {

      dataList.value = response.data[0]

    } else {

      dataList.value = response.data

    }

    console.log(dataList.value)

  } catch (error) {

    console.error(error)

  }
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

  <style>

.card-logo {
  height: 30px;
  width: 30px;
  margin-right: 10px;
}

.card-title {
  display: flex;
  align-items: center;
  font-size: 20px;
}
  </style>

</template>