<template>
  <div>
    <h1>Emoji Password</h1>
    <div>
      <div :class="{ 'strikethrough': passwordStatus[0].used === 1 }">113.573424,34.814508</div>
      <div :class="{ 'strikethrough': passwordStatus[1].used === 1 }">113.547963,34.747164</div>
      <div :class="{ 'strikethrough': passwordStatus[2].used === 1 }">113.620766,34.742025</div>
    </div>
    <div>
      <input type="text" v-model="password[0]"/>
      <input type="text" v-model="password[1]"/>
      <input type="text" v-model="password[2]"/>
    </div>
    <button @click="submitPassword">Submit</button>
    <div v-if="showSuccess" class="success">Success!</div>
    <div v-if="showError" class="error">Error!</div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

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

    onMounted(() => {
      fetchPasswordStatus();
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
.success {
  color: green;
}
.error {
  color: red;
}
.strikethrough {
  text-decoration: line-through;
}
</style>