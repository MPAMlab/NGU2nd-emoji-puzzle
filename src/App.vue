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
        <div :class="{ 'strikethrough': passwordStatus[0].used === 1 }" class="play-regular">113.573424,34.814508</div>
        <div :class="{ 'strikethrough': passwordStatus[0].used === 1 }" class="play-regular">113.547963,34.747164</div>
        <div :class="{ 'strikethrough': passwordStatus[0].used === 1 }" class="play-regular">113.620766,34.742025</div>
      </div>
      <div class="emoji-inputs">
        <input type="text" v-model="password[0]" />
        <input type="text" v-model="password[1]" />
        <input type="text" v-model="password[2]" />
      </div>
      <button @click="submitPassword">Submit</button>
      <div v-if="showSuccess" class="success">Success!</div>
      <div v-if="showError" class="error">Error!</div>
    </div>
    <footer>
      <img src="./assets/footer.webp" alt="Footer Image" />
    </footer>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { onBeforeUnmount } from 'vue';
export default {
  setup() {
    const password = ref(['', '', '']);
    const showSuccess = ref(false);
    const showError = ref(false);
    const passwordStatus = ref([
      { used: 0 },
      { used: 0 },
      { used: 0 },
    ]);

    const submitPassword = async () => {
      showSuccess.value = false;
      showError.value = false;

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
          fetchPasswordStatus(); // Update the password status after successful submission
        } else {
          showError.value = true;
          console.error('Error:', data.error);
        }
      } catch (error) {
        showError.value = true;
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
    const scaleContent = () => {
      const backgroundImg = document.querySelector('.background-image img');
      if (backgroundImg) {
        const idealWidth = 770; // 定义理想宽度
        const currentWidth = backgroundImg.offsetWidth; // 获取当前宽度
        const scaleFactor = currentWidth / idealWidth; // 计算缩放因子
        const contentDiv = document.querySelector('.content');
        if (contentDiv) {
          contentDiv.style.transform = `translate(-50%, -50%) scale(${scaleFactor})`;
        }
      }
    };
    onMounted(() => {
      fetchPasswordStatus();
      scaleContent(); // 页面加载时缩放内容
      window.addEventListener('resize', scaleContent); // 窗口大小改变时重新缩放内容
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
    };
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Play:wght@400;700&display=swap');
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
  /* transform: translate(-50%, -50%); 不再需要这里，因为它会在 JS 中设置 */
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
  top: -150px; /* 调整此值以控制与 emoji-inputs 的距离 */
  left: 50%;
  transform: translateX(-50%);
  border-radius: 5px;
}

.emoji-inputs {
  display: flex;
}
button {
  position: absolute;
  bottom: -90px; /* 调整此值以控制与 emoji-inputs 的距离 */
  left: 50%;
  transform: translateX(-50%);
}
.emoji-inputs input {
  width: 50px;
  height: 50px;
  font-size: 24px;
  text-align: center;
  margin: 0 25px;
}

.success {
  color: green;
}

.error {
  color: red;
}

.strikethrough {
  text-decoration: line-through;
}
.play-regular {
  font-family: "Play", sans-serif;
  font-weight: 400;
  font-style: normal;
}
</style>