<!-- SuccessModal.vue -->
<template>
    <div class="success-modal">
      <div class="success-modal-content">
        <img :src="image" alt="Success Modal Image" />
        <button @click="closeModal" class="btn">关闭</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      image: {
        type: String,
        required: true,
      },
    },
    emits: ['close-modal'],
    methods: {
      closeModal() {
        this.$emit('close-modal');
      },
    },
  };
  </script>
  
  <style scoped>
  .success-modal {
    position: fixed;
    z-index: 4;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0); /* 背景设置为透明 */
  }
  
  .success-modal-content {
    position: relative;
    text-align: center;
  }
  
  .success-modal-content img {
    max-width: 70%;
    max-height: 70%;
  }
  
  .btn {
    margin-top: 20px;
  }
  </style>