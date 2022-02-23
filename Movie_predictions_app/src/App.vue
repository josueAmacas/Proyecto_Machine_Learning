<template>
  <v-app style="background-image: url('https://w7.pngwing.com/pngs/275/309/png-transparent-cinema-film-popcorn-food-film-poster-clapperboard.png');background-repeat: repeat;">
    <v-main>
      <HelloWorld/>
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld';

export default {
  name: 'App',

  components: {
    HelloWorld,
  },

  data: () => ({
    //
  }),
};
</script>

