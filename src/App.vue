<template>
  <div class="container">
    <header>
      <img src="./assets/header.webp" alt="Header Image" />
    </header>
    <div class="background">
      <div class="animation-background">
        <img src="./assets/grid.webp" alt="Animation Background" />
      </div>
      <div class="background-image">
        <img src="./assets/background-image.webp" alt="Background Image" />
      </div>
    </div>
    <div class="content">
      <div class="password-status">
        <div
          :class="{ strikethrough: passwordStatus[0].used === 1, link: passwordStatus[0].used === 1 }"
          class="play-regular"
          @click="openModal(passwordStatus[0].image, passwordStatus[0].text, 0)"
        >
          113.573424,34.814508
        </div>
        <div
          :class="{ strikethrough: passwordStatus[1].used === 1, link: passwordStatus[1].used === 1 }"
          class="play-regular"
          @click="openModal(passwordStatus[1].image, passwordStatus[1].text, 1)"
        >
          113.547963,34.747164
        </div>
        <div
          :class="{ strikethrough: passwordStatus[2].used === 1, link: passwordStatus[2].used === 1 }"
          class="play-regular"
          @click="openModal(passwordStatus[2].image, passwordStatus[2].text, 2)"
        >
          113.620766,34.742025
        </div>
      </div>
      <div class="emoji-inputs">
        <input type="text" v-model="password[0]" />
        <input type="text" v-model="password[1]" />
        <input type="text" v-model="password[2]" />
      </div>
      <button @click="submitPassword" class="btn">Submit</button>
    </div>
    <footer>
      <img src="./assets/footer.webp" alt="Footer Image" />
    </footer>
    <!-- 成功弹窗 -->
    <SuccessModal v-if="showSuccessModal" :image="modalImage" @close-modal="closeModal" />

    <!-- 错误弹窗 -->
    <div v-if="showErrorModal" class="error-modal">
      <div class="error-modal-content">
        <p v-if="modalText">{{ modalText }}</p>
        <p v-else>输入错误或格式不正确</p>
        <button @click="closeModal" class="btn">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { onBeforeUnmount } from 'vue';
import SuccessModal from './components/SuccessModal.vue';
export default {
  components: {
    SuccessModal,
  },
  setup() {
    const password = ref(['', '', '']);
    const showSuccess = ref(false);
    const showError = ref(false);
    const showSuccessModal = ref(false);
    const showErrorModal = ref(false);
    const passwordStatus = ref([
      { used: 0 },
      { used: 0 },
      { used: 0 },
    ]);
    const modalImage = ref('');
    const modalText = ref('');

    const submitPassword = async () => {
      showSuccessModal.value = false;
      showErrorModal.value = false;


      try {
        const unicodePassword = password.value.map(char => char.codePointAt(0).toString(16).padStart(4, '0'));

        const response = await fetch('https://qos6gq6i3f.execute-api.ap-northeast-1.amazonaws.com/default/emoji-puzzle', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ password: unicodePassword }),
        });

        const data = await response.json();

        if (response.ok) {
          showSuccess.value = true;
          fetchPasswordStatus(); // 更新密码状态后显示弹窗
          showSuccessModal.value = true;
          modalImage.value = data.image;
        } else {
          showError.value = true;
          showErrorModal.value = true; // 显示错误弹窗
          modalText.value = data.error;
          console.error('Error:', data.error);
        }
      } catch (error) {
        showError.value = true;
        showErrorModal.value = true; // 显示错误弹窗
        console.error('Error:', error);
      }
    };

    const fetchPasswordStatus = async () => {
      try {
        const response = await fetch('https://qos6gq6i3f.execute-api.ap-northeast-1.amazonaws.com/default/emoji-puzzle', {
          method: 'GET',
        });

        const data = await response.json();

        if (response.ok) {
          passwordStatus.value = data;
        } else {
          console.error('Error:', data.error);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };
    const openModal = (image, text, index) => {
      if (passwordStatus.value[index].used === 0) {
    return; // 如果密码已经被使用，则不执行后续代码
    }
      showSuccessModal.value = true;
      modalImage.value = image;
      modalText.value = text;
    };
    const closeModal = () => {
      showSuccessModal.value = false;
      showErrorModal.value = false;
      modalImage.value = '';
      modalText.value = '';
    };

    const scaleContent = () => {
      const backgroundImg = document.querySelector('.background-image img');
      if (backgroundImg) {
        const idealWidth = 770; // 定义理想宽度
        const currentWidth = backgroundImg.offsetWidth; // 获取当前宽度
        if (currentWidth > idealWidth) {
          const scaleFactor = currentWidth / idealWidth; // 计算缩放因子
          const contentDiv = document.querySelector('.content');
          if (contentDiv) {
            contentDiv.style.transform = `translate(-50%, -50%) scale(${scaleFactor})`;
          }
        } else {
          const contentDiv = document.querySelector('.content');
          if (contentDiv) {
            contentDiv.style.transform = 'translate(-50%, -50%)';
          }
        }
      }
    };

    onMounted(() => {
      fetchPasswordStatus();
      scaleContent();
      window.addEventListener('resize', scaleContent);
    });

    onBeforeUnmount(() => {
      window.removeEventListener('resize', scaleContent);
    });

    return {
      password,
      submitPassword,
      showSuccess,
      showError,
      passwordStatus,
      showSuccessModal,
      showErrorModal,
      modalImage,
      modalText,
      closeModal,
      openModal,
    };
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Play:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@100..900&display=swap');
body, html {
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
}

.container {
    position: relative;
    min-height: 100vh;
}

header, footer {
    position: absolute;
    left: 0;
    right: 0;
    z-index: 2;
}

header {
    top: 0;
}

header img {
    width: 100%;
    height: auto;
}

footer {
    bottom: 0;
}

footer img {
    width: 100%;
    height: auto;
}

.background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    z-index: 0;
}

.animation-background,
.background-image {
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.animation-background img,
.background-image img {
    flex-shrink: 0;
    min-width: 0;
    min-height: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}
@-webkit-keyframes fadeAnimation {
    0% {
        opacity: 0;
        -webkit-filter: brightness(2);
        filter: brightness(2);
    }
    50% {
        opacity: 1;
        -webkit-filter: brightness(1);
        filter: brightness(1);
    }
    100% {
        opacity: 0;
        -webkit-filter: brightness(2);
        filter: brightness(2);
    }
}

@keyframes fadeAnimation {
    0% {
        opacity: 0;
        -webkit-filter: brightness(2);
        filter: brightness(2);
    }
    50% {
        opacity: 1;
        -webkit-filter: brightness(1);
        filter: brightness(1);
    }
    100% {
        opacity: 0;
        -webkit-filter: brightness(2);
        filter: brightness(2);
    }
}

.animation-background img {
    -webkit-animation: fadeAnimation 5s infinite;
    animation: fadeAnimation 5s infinite;
}
.animation-background {
    z-index: 1;
}

.content {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 3;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.password-status {
    background-color: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(5px);
    padding: 20px;
    position: absolute;
    top: -150px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 5px;
}

.emoji-inputs {
    display: flex;
    justify-content: center;
    align-items: center;
}

.input-wrapper{
  width: 50px;
  height: 50px;
     margin: 0 3.5vh;
   position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}
.custom-input {
    width: 55px;
    height: 55px;
    font-size: 24px;
    text-align: center;
    background-color: rgba(255,255,255,0.3);
    border: 1px solid #fff;
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
     padding: 0;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(30deg);
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
    -webkit-appearance: none;
       -moz-appearance: none;
            appearance: none;
}

.custom-input:focus {
    outline: none;
    box-shadow: 0 0 10px rgba(255,255,255,0.5);
}
button {
  position: absolute;
  bottom: -90px;
  left: 50%;
  transform: translateX(-50%);
}
.btn,
.btn:focus {
    min-width: 200px;
    background: transparent;
    color: #FFFFFF;
    font-size: 1rem;
    text-align: center;
    text-transform: uppercase;
    text-decoration: none;
    box-sizing: inherit;
    padding: 10px 20px;
    border: 1px solid;
    box-shadow: inset 0 0 20px rgba(225, 51, 45, 0);
    outline: 1px solid !important;
    outline-color: rgba(225, 51, 45, 0.5);
    outline-offset: 0px;
    text-shadow: none;
    transition: all 1250ms cubic-bezier(0.19, 1, 0.22, 1);
    backdrop-filter: blur(8px);
    font-family: "Play", sans-serif;
    font-weight: 400;
    font-style: normal;
}
.btn:hover {
    color: #E1332D;
    border: 1px solid;
    box-shadow: inset 0 0 20px rgba(225, 51, 45, 0.5), 0 0 20px rgba(225, 51, 45, 0.2);
    outline: 1px solid !important;
    outline-color: rgba(225, 51, 45, 0) !important;
    outline-offset: 15px;
    text-shadow: 1px 1px 2px #427388;
}


.success {
  color: green;
}

.error {
  color: red;
}

.strikethrough {
  color: green;
}
.link {
  cursor: pointer;
  text-decoration: underline;
}
.play-regular {
  font-family: "Play", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.modal {
  position: fixed;
  z-index: 4;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  margin: 15% auto;
  padding: 20px;
  width: 80%;
  max-width: 600px;
  position: relative;
  text-align: center;
}
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}
.error-modal {
  position: fixed;
  z-index: 4;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.4);
}

.error-modal-content {
  background-color: rgba(255, 255, 255, 0.20);
  backdrop-filter: blur(10px);
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 600px;
  position: relative;
  text-align: center;
  border-radius: 5px;
  font-family: "Noto Sans SC", sans-serif;
  font-optical-sizing: auto;
}
.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.modal-content img {
  max-width: 100%;
  height: auto;
}
</style>