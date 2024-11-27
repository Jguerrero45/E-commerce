<script setup>
import { ref, onMounted } from 'vue';
import $ from 'jquery';
import 'datatables.net';
import 'datatables.net-dt/css/dataTables.dataTables.css';
import apiClient from '../api/api.js';

const products = ref([]); // Lista de productos
const table = ref(null); // Referencia a la tabla
const selectedProduct = ref(null); // Producto seleccionado para editar o ver
const modalMode = ref('create'); // Modo del modal: create | edit | view
const showModal = ref(false); // Controla la visibilidad del modal

// Campos del formulario
const title = ref('');
const description = ref('');
const price = ref('');
const sku = ref('');
const barcode = ref('');
const stock = ref('');
const brand = ref('');
const category = ref('');
const images = ref('');
const thumbnail = ref('');
const dimensions = ref({ width: null, height: null, depth: null });

// Función para obtener productos
const fetchProducts = async () => {
  try {
    const response = await apiClient.get('/products/');
    products.value = response.data;
    initializeDataTable();
  } catch (error) {
    console.error('Error al cargar los productos:', error);
  }
};

// Función para eliminar un producto
const deleteProduct = async (id) => {
  try {
    await apiClient.delete(`/products/${id}/`);
    alert(`Producto con ID ${id} eliminado exitosamente.`);
    fetchProducts(); // Recarga los datos
  } catch (error) {
    console.error(`Error al eliminar el producto con ID ${id}:`, error);
    alert('No se pudo eliminar el producto. Inténtalo de nuevo.');
  }
};

// Función para abrir el modal
const openModal = (product = null, mode = 'create') => {
  selectedProduct.value = product ? { ...product } : null;
  modalMode.value = mode;

  if (mode !== 'create' && product) {
    title.value = product.title || '';
    description.value = product.description || '';
    price.value = product.price || '';
    sku.value = product.sku || '';
    barcode.value = product.meta_info?.barcode || '';
    stock.value = product.stock || '';
    brand.value = product.brand || '';
    category.value = product.category || '';
    images.value = product.images.join(', ') || '';
    thumbnail.value = product.thumbnail || '';
    dimensions.value = {
      width: product.dimensions?.width || null,
      height: product.dimensions?.height || null,
      depth: product.dimensions?.depth || null,
    };
  } else {
    // Reinicia los campos para creación
    title.value = '';
    description.value = '';
    price.value = '';
    sku.value = '';
    barcode.value = '';
    stock.value = '';
    brand.value = '';
    category.value = '';
    images.value = '';
    thumbnail.value = '';
    dimensions.value = { width: null, height: null, depth: null };
  }

  showModal.value = true;
};

// Función para cerrar el modal
const closeModal = () => {
  showModal.value = false;
};

// Función para guardar cambios en un producto
const saveProductChanges = async () => {
  try {
    const updatedProduct = {
      title: title.value,
      description: description.value,
      price: price.value,
      sku: sku.value,
      stock: stock.value,
      brand: brand.value,
      category: category.value,
      images: images.value.split(','),
      thumbnail: thumbnail.value,
      dimensions: dimensions.value,
    };
    await apiClient.put(`/products/${selectedProduct.value.id}/`, updatedProduct);
    alert('Producto actualizado exitosamente.');
    closeModal();
    fetchProducts();
  } catch (error) {
    console.error('Error al actualizar el producto:', error);
    alert('Error al actualizar el producto.');
  }
};

// Función para manejar el envío del formulario
const handleSubmit = () => {
  if (modalMode.value === 'edit') {
    saveProductChanges();
  } else if (modalMode.value === 'create') {
    createProduct();
  }
};

// Inicializar DataTable
const initializeDataTable = () => {
  if (table.value) {
    $(table.value).DataTable({
      data: products.value,
      columns: [
        { data: 'title', title: 'Nombre' },
        { data: 'description', title: 'Descripción' },
        { data: 'price', title: 'Precio' },
        {
          data: null,
          title: 'Acciones',
          orderable: false,
          render: (data, type, row) => `
            <button class="edit-btn" data-id="${row.id}">Editar</button>
            <button class="view-btn" data-id="${row.id}">Ver</button>
            <button class="delete-btn" data-id="${row.id}">Eliminar</button>
          `,
        },
      ],
      destroy: true,
      responsive: true,
      drawCallback: function () {
        $('.edit-btn').off('click').on('click', function () {
          const productId = $(this).data('id');
          const product = products.value.find((p) => p.id === productId);
          openModal(product, 'edit');
        });

        $('.view-btn').off('click').on('click', function () {
          const productId = $(this).data('id');
          const product = products.value.find((p) => p.id === productId);
          openModal(product, 'view');
        });

        $('.delete-btn').off('click').on('click', function () {
          const productId = $(this).data('id');
          deleteProduct(productId);
        });
      },
    });
  }
};

onMounted(() => {
  fetchProducts();
});
</script>

<template>
  <div>
    <table ref="table"></table>

    <div v-if="showModal">
      <form v-if="modalMode !== 'view'" @submit.prevent="handleSubmit">
        <input v-model="title" placeholder="Título" />
        <textarea v-model="description" placeholder="Descripción"></textarea>
        <input v-model="price" type="number" placeholder="Precio" />
        <!-- Más campos aquí -->
        <button type="submit">{{ modalMode === 'edit' ? 'Guardar Cambios' : 'Crear' }}</button>
        <button type="button" @click="closeModal">Cancelar</button>
      </form>

      <div v-if="modalMode === 'view'">
        <h2>{{ title }}</h2>
        <p>{{ description }}</p>
        <p><strong>Precio:</strong> {{ price }}</p>

        <button type="button" @click="closeModal">Cerrar</button>
      </div>
    </div>
  </div>
</template>