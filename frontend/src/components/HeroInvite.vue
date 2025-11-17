<script setup>
const emit = defineEmits(['browse'])

function handleBrowse() {
  emit('browse')
}
</script>

<template>
  <section class="hero-wrapper q-mb-xl">
    <q-card class="hero-card q-pa-xl">
      <div class="row items-center q-col-gutter-xl full-height">
        <div class="col-12 col-md-7">
          <div class="text-overline text-weight-bold hero-tag q-mb-sm">
            Pet sitting made easy
          </div>

          <div class="text-h3 text-weight-bold q-mb-md hero-title">
            Help owners.  
            <span class="text-weight-bolder">Spend time with pets.</span>
          </div>

          <div class="text-body1 q-mb-lg hero-text">
            Browse pets looking for a sitter, schedule safe appointments, and keep everything
            organized in one place. Perfect for animal lovers who want to help out (and get some
            extra cuddles).
          </div>

          <div class="row items-center q-gutter-sm">
            <q-btn
              color="primary"
              unelevated
              icon="pets"
              label="Browse pets"
              size="lg"
              @click="handleBrowse"
            />
            <q-btn
              flat
              color="primary"
              label="See upcoming appointments"
              icon="event"
              @click="handleBrowse"
            />
          </div>
        </div>

        <div class="col-12 col-md-5 hero-side-panel column items-center justify-center">
          <q-icon name="favorite" size="64px" class="q-mb-md" />
          <div class="text-h6 text-center q-mb-sm">
            Join our pet sitting community
          </div>
          <div class="text-body2 text-center">
            Choose a pet, agree on a time, and enjoy some quality time together — while owners get
            peace of mind knowing their pets are in good hands.
          </div>
        </div>
      </div>
    </q-card>
  </section>
</template>

<style scoped>
.hero-wrapper {
  /* Give the hero vertical presence relative to viewport */
  min-height: 70vh;
  display: flex;
  align-items: center;
}

/* Card fills most of that space */
.hero-card {
  width: 100%;
  border-radius: 24px;
  border: 1px solid rgba(167, 190, 174, 0.8); /* #A7BEAE */
  background: linear-gradient(
    135deg,
    #e7e8d1 0%,
    #f7f8ec 40%,
    #ffffff 100%
  );
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.hero-tag {
  color: #b85042;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.hero-title {
  color: #2b2c28;
}

.hero-text {
  color: #4b4b42;
  max-width: 38rem;
}

.hero-side-panel {
  border-radius: 18px;
  padding: 20px;
  background: rgba(184, 80, 66, 0.06); /* soft #B85042 */
  color: #2b2c28;
}

/* Dark mode tweaks */
body.body--dark .hero-card {
  background: radial-gradient(circle at top left, #3a3c35 0%, #2b2c28 60%, #1f201c 100%);
  border-color: #a7beae;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
}

body.body--dark .hero-title,
body.body--dark .hero-text {
  color: #e7e8d1;
}

body.body--dark .hero-side-panel {
  background: rgba(167, 190, 174, 0.12);
  color: #e7e8d1;
}
</style>
