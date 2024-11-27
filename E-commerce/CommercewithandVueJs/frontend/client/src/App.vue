<!-- src/App.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import Modal from './components/Modal.vue'
import Datatable from './components/Datatable.vue';
import apiClient from './api/api.js'
import Multiselect from 'vue-multiselect'

const value = ref([])
const options = ref([])

const showModal = ref(false)


const barcode = ref('')
const sku = ref('')
const thumbnail = ref('')
const qrCode = ref('')
const title = ref('')
const description = ref('')
const category = ref('')
const price = ref(null)
const discountPercentage = ref(null)
const rating = ref(null)
const stock = ref(null)
const minimumOrderQuantity = ref(null)
const warrantyInformation = ref('')
const shippingInformation = ref('')
const availabilityStatus = ref('')
const returnPolicy = ref('')
const images = ref([])
const dimensions = ref({ width: null, height: null, depth: null })
const brand = ref('')
const weight = ref(null)


const openModal = () => {
  showModal.value = true
}


const closeModal = () => {
  showModal.value = false
}

const loadTags = async () => {
  try {
    const response = await apiClient.get('/tags/');
    options.value = response.data.map(tag => ({
      name: tag.name,
      code: tag.id.toString()
    }));
  } catch (error) {
    console.error('Error al cargar las etiquetas:', error);
  }
};

onMounted(() => {
  loadTags();
});

const addTag = async (newTag) => {
  const existingTag = options.value.find(tag => tag.name === newTag);
  if (existingTag) {
    value.value.push(existingTag);
    return;
  }

  try {
    const response = await apiClient.post('/tags/', { name: newTag });
    const tag = {
      name: response.data.name,
      code: response.data.id.toString(),
    };
    options.value.push(tag);
    value.value.push(tag);
  } catch (error) {
    console.error('Error al crear la etiqueta:', error);
  }
};

const validateBarcode = () => {
  const barcodeStr = barcode.value?.toString().padStart(13, '0') || '';
  if (barcodeStr.length !== 13) {
    console.warn("El código de barras no tiene exactamente 13 dígitos.");
    alert('El código de barra debe tener exactamente 13 dígitos.');
    return false;
  }

  console.log("El código de barras es válido.");
  return true;
};

const validateSku = () => {
  if (sku.value.length !== 8) {
    alert('El SKU debe tener exactamente 8 caracteres.')
    return false
  }
  return true
}

const handleSubmit = async () => {
  const isBarcodeValid = validateBarcode()
  const isSkuValid = validateSku()

  if (isBarcodeValid && isSkuValid) {
    const productData = {
      title: title.value || '',
      description: description.value || '',
      category: category.value || '',
      price: parseFloat(price.value) || 0,
      discount_percentage: parseFloat(discountPercentage.value) || 0,
      rating: parseFloat(rating.value) || 0,
      stock: parseInt(stock.value, 10) || 0,
      tags: value.value.map(tag => ({ name: tag.name })),
      sku: sku.value || '',
      warranty_information: warrantyInformation.value || '',
      shipping_information: shippingInformation.value || '',
      availability_status: availabilityStatus.value || '',
      return_policy: returnPolicy.value || '',
      minimum_order_quantity: parseInt(minimumOrderQuantity.value, 10) || 1,
      images: images.value.length > 0
        ? images.value.split(',').map(url => url.trim())
        : [],
      thumbnail: thumbnail.value || '',
      dimensions: {
        width: parseFloat(dimensions.value.width) || 0,
        height: parseFloat(dimensions.value.height) || 0,
        depth: parseFloat(dimensions.value.depth) || 0,
      },
      meta_info: {
        barcode: parseInt(barcode.value, 10) || 0,
        qr_code: qrCode.value || '',
      },
      brand: brand.value || '',
      weight: parseFloat(weight.value) || 0,
    };
    console.log('Datos del producto:', productData);
    try {
      const response = await apiClient.post('/products/', productData)
      console.log('Producto creado:', response.data)
      alert('Producto creado exitosamente.')
      closeModal()
    } catch (error) {
      console.error('Error al crear el producto:', error)
      alert('Ocurrió un error al crear el producto.')
    }
  } else {
    console.error('Errores en el formulario')
  }
}
</script>

<template>
  <div class=" m-5">
    <h1 class="text-form">Manejador de productos</h1>
    <button @click="openModal">Crear un producto</button>
    <transition name="modal">
      <Modal v-if="showModal" @close="closeModal">
        <form @submit.prevent="handleSubmit">
          <h2 class="text-form my-5">Informacion de producto</h2>
          <input class="input w-full m-1" placeholder="Nombre" type="text" v-model="title">
          <textarea class="input w-full m-1" placeholder="Descripcion" rows="2" v-model="description"></textarea>
          <multiselect 
            v-model="value" 
            tag-placeholder="Add this as new tag" 
            placeholder="Search or add a tag" 
            label="name"
            track-by="code" 
            :options="options" 
            :multiple="true" 
            :taggable="true" 
            @tag="addTag"
            class="m-1">
          </multiselect>
          <input class="input w-[23.6%] m-1" placeholder="Precio" type="number" step="0.01" v-model="price">
          <input class="input w-[23.6%] m-1" placeholder="Descuento" type="number" step="0.01" v-model="discountPercentage">
          <input class="input w-[23.6%] m-1" placeholder="Puntuacion" type="number" step="0.1" v-model="rating">
          <input class="input w-[23.6%] m-1" placeholder="Stock" type="number" v-model="stock">
          <input class="input w-[31.9%] m-1" placeholder="Marca" type="text" v-model="brand">
          <input class="input w-[31.9%] m-1" placeholder="Peso" type="number" step="0.01" v-model="weight">
          <input class="input w-[31.9%] m-1" placeholder="Categoria" type="text" step="0.01" v-model="category">
          <input class="input w-[48.6%] m-1" placeholder="Cantidad minima de ordenes" type="number" v-model="minimumOrderQuantity">
          <input class="input w-[48.6%] m-1" placeholder="SKU" type="text" v-model="sku">
          <input class="input w-[48.6%] m-1" placeholder="Informacion de garantia" type="text" v-model="warrantyInformation">
          <input class="input w-[48.6%] m-1" placeholder="Informacion de envio" type="text" v-model="shippingInformation">
          <input class="input w-[48.6%] m-1" placeholder="Politica de retorno" type="text" v-model="returnPolicy">
          <input class="input w-[48.6%] m-1" placeholder="Estatus de disponibilidad" type="text" v-model="availabilityStatus">
          <input class="input w-[48.6%] m-1" placeholder="Imagenes" type="text" v-model="images">
          <input class="input w-[48.6%] m-1" placeholder="Miniatura" type="url" v-model="thumbnail">
          <h2 class="text-form my-0.5">Dimensiones</h2>
          <input class="input w-[31.9%] m-1" placeholder="Ancho" type="number" step="0.01" v-model="dimensions.width">
          <input class="input w-[31.9%] m-1" placeholder="Alto" type="number" step="0.01" v-model="dimensions.height">
          <input class="input w-[31.9%] m-1" placeholder="Profundidad" type="number" step="0.01" v-model="dimensions.depth">
          <h2 class="text-form my-0.5">MetaInfo</h2>
          <input class="input w-[48.6%] m-1" placeholder="Código de barra" type="number" v-model="barcode">
          <input class="input w-[48.6%] m-1" placeholder="Código QR" type="url" v-model="qrCode">
          <div class="button-container">
            <button type="submit">Agregar</button>
          </div>
        </form>
      </Modal>
    </transition>
    <Datatable/>
  </div>

</template>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
body {
  background-color: #ffffff; /* Gris claro */
  font-family: Arial, sans-serif;
  color: #000000; /* Color de texto oscuro para mejor contraste */
}

.text-form {
  font-size: 20px;
  font-weight: bold;
  color: #41b883;
  text-align: center;
}

.input {
  border: none;
  outline: none;
  border-radius: 15px;
  padding: 1em;
  background-color: #ccc;
  box-shadow: inset 2px 5px 10px rgba(0,0,0,0.3);
  transition: 300ms ease-in-out;
  font-size: 16px;
}

.input:focus {
  background-color: white;
  transform: scale(1.05);
  box-shadow: 13px 13px 100px #969696,
             -13px -13px 100px #ffffff;
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.modal-enter-to, .modal-leave-from {
  opacity: 1;
  transform: scale(1);
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.button-container {
  display: flex;
  justify-content: center; 
}

button {
  position: relative;
  display: inline-block;
  margin: 15px;
  padding: 15px 30px;
  text-align: center;
  font-weight: bold;
  font-size: 18px;
  letter-spacing: 1px;
  text-decoration: none;
  color: #41b883;
  background: transparent;
  cursor: pointer;
  transition: ease-out 0.5s;
  border: 2px solid #41b883;
  border-radius: 10px;
  box-shadow: inset 0 0 0 0 #41b883;
}

button:hover {
  color: white;
  box-shadow: inset 0 -100px 0 0 #41b883;
}

button:active {
  transform: scale(0.9);
}

.multiselect__input {
  font-size: 16px !important; 
}
</style>