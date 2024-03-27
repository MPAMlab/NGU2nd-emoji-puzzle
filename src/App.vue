<template>
  <div>
    <h1>Emoji Password</h1>
    <div>
      <div :class="{ 'strikethrough': passwordStatus[0].used === 1 }">文本一</div>
      <div :class="{ 'strikethrough': passwordStatus[1].used === 1 }">文本二</div>
      <div :class="{ 'strikethrough': passwordStatus[2].used === 1 }">文本三</div>
    </div>
    <div>
      <input
        type="text"
        v-model="password[0]"
        @input="enforceEmojiInput(0, $event)"
        maxlength="1"
      />
      <input
        type="text"
        v-model="password[1]"
        @input="enforceEmojiInput(1, $event)"
        maxlength="1"
      />
      <input
        type="text"
        v-model="password[2]"
        @input="enforceEmojiInput(2, $event)"
        maxlength="1"
      />
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

    const enforceEmojiInput = (index, event) => {
      const input = event.target.value;
      if (input.length === 1 && !isEmoji(input)) {
        password.value[index] = '';
      }
    };

    const isEmoji = (str) => {
      const regex = /(?:\[\u2700-\u27bf\]|(?:\ud83c[\udde6-\uddff]){2}|[\ud800-\udbff][\udc00-\udfff]|[\u0023-\u0039]\ufe0f?\u20e3|\u3299|\u3297|\u303d|\u3030|\u24c2|\ud83c[\udd70-\udd71]|\ud83c[\udd7e-\udd7f]|\ud83c\udd8e|\ud83c[\udd91-\udd9a]|\ud83c[\udde6-\uddff]|[\ud83c\ude01-\ude02]|\ud83c\ude1a|\ud83c\ude2f|[\ud83c\ude32-\ude3a]|[\ud83c\ude50-\ude51]|\u203c|\u2049|[\u25aa-\u25ab]|\u25b6|\u25c0|[\u25fb-\u25fe]|\u00a9|\u00ae|\u2122|\u2139|\ud83c\udc04|[\u2600-\u26FF]|\u2b05|\u2b06|\u2b07|\u2b1b|\u2b1c|\u2b50|\u2b55|\u231a|\u231b|\u2328|\u23cf|[\u23e9-\u23f3]|[\u23f8-\u23fa]|\ud83c\udccf|\u2934|\u2935|[\u2190-\u21ff])/g;
      return regex.test(str);
    };

    const submitPassword = async () => {
      showSuccess.value = false;
      showError.value = false;

      try {
        const response = await fetch('https://qos6gq6i3f.execute-api.ap-northeast-1.amazonaws.com/default/emoji-puzzle', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ password: password.value }),
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
      enforceEmojiInput,
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