<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12" sm="12" md="12">
        <v-card>
          <v-img
            :src="`https://s3-us-west-2.amazonaws.com/prd-rteditorial/wp-content/uploads/2018/03/13153742/RT_300EssentialMovies_700X250.jpg`"
            height="500px"
          >
          </v-img>
          <v-card-title class="text-center justify-center py-6">
            <h1 class="font-weight-bold text-h2 basil--text">
              MoviePredictions
            </h1>
          </v-card-title>

          <v-tabs
            v-model="tab"
            background-color="transparent"
            color="basil"
            grow
          >
            <v-tab v-for="(item, i) in items" :key="i">
              {{ item.item }}
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab">
            <v-tab-item v-for="(item, i) in items" :key="i">
              <v-card color="basil" flat>
                <center>
                  <v-card-title>{{ item.text }}</v-card-title>
                </center>

                <v-card-text v-if="i == 0">
                  <v-row>
                    <v-col md="4">
                      <v-select
                        v-model="movie"
                        :items="list_movies_str"
                        chips
                        label="List Movies"
                        outlined
                        @change="movie_select()"
                      >
                        <template v-slot:item="{ item }">
                          {{ item.Title }}
                        </template>
                        <template v-slot:selection="{ item }">
                          <v-chip>
                            {{ item.Title }}
                          </v-chip>
                        </template>
                      </v-select>
                      <v-text-field
                        v-model="votes"
                        label="Votes"
                        type="number"
                        readonly
                        required
                        outlined
                      ></v-text-field>
                      <v-text-field
                        v-model="duration"
                        label="Duration"
                        type="number"
                        readonly
                        required
                        outlined
                      ></v-text-field>
                      <v-text-field
                        v-model="budget_code"
                        label="Budget Code"
                        readonly
                        required
                        type="number"
                        outlined
                      ></v-text-field>
                      
                    </v-col>
                    <v-col md="8">
                      <v-list>
                        <v-subheader inset
                          ><center>
                            <strong style="font-zize: 2vh">Result</strong>
                          </center>
                        </v-subheader>
                        <v-divider></v-divider>
                        <v-list-item>
                          <v-list-item-avatar width="50%">
                            <v-chip
                              class="primary"
                              dark
                              v-text="precition_result"
                            ></v-chip>
                          </v-list-item-avatar>

                          <v-list-item-content>
                            <v-list-item-title
                              v-text="precition_text"
                            ></v-list-item-title>

                            <v-list-item-subtitle
                              v-text="'MoviePredictions'"
                            ></v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                        <v-divider></v-divider>
                        <v-list-item>
                          <v-list-item-avatar width="50%">
                            <v-chip
                              class="primary"
                              dark
                              v-text="rating_IMDb_result"
                            ></v-chip>
                          </v-list-item-avatar>

                          <v-list-item-content>
                            <v-list-item-title
                              v-text="rating_IMDb_text"
                            ></v-list-item-title>

                            <v-list-item-subtitle
                              v-text="'MoviePredictions'"
                            ></v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                      </v-list>
                    </v-col>
                  </v-row>
                </v-card-text>
                <v-card-text v-if="i == 1">
                  <v-row>
                    <v-col md="8">
                      <v-simple-table fixed-header>
                        <template v-slot:default>
                          <thead>
                            <tr>
                              <th class="text-center"><strong>Title</strong> </th>
                              <th class="text-center"><strong>Score</strong> </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="item in list_movie_r" :key="item.name">
                              <td>{{ item.Title }}</td>
                              <td><v-chip
                              class="primary"
                              dark
                              v-text="item.Score"
                            ></v-chip></td>
                            </tr>
                          </tbody>
                        </template>
                      </v-simple-table>
                    </v-col>
                    <v-col md="3">
                      <v-select
                        v-model="movie_r"
                        :items="list_movies_str"
                        chips
                        label="List Movies"
                        outlined
                        @change="movie_select_r()"
                      >
                        <template v-slot:item="{ item }">
                          {{ item.Title }}
                        </template>
                        <template v-slot:selection="{ item }">
                          <v-chip>
                            {{ item.Title }}
                          </v-chip>
                        </template>
                      </v-select>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
var ENDPOINT_PATH = "https://movie-predictions-server.herokuapp.com";
var http = axios.create({
  baseURL: ENDPOINT_PATH,
});
import axios from "axios";
export default {
  name: "HelloWorld",

  data: () => ({
    tab: null,
    items: [
      { item: "Reating IMBd", text: "Modelo De Regression" },
      { item: "Recomendation Movies", text: "Modelo De Clasificación" },
    ],
    votes: 0.0,
    duration: 0.0,
    budget_code: 0.0,
    rating: 0.0,

    precition_result: 0,
    precition_text: "Absolute Mean Error",
    rating_IMDb_result: 0,
    rating_IMDb_text: "Rating IMDb",

    list_movies_str: [],
    movie: [],
    movie_r: [],
    list_movie_r: [],
    title: "",
  }),
  mounted() {
    this.list_movies();
  },
  methods: {
    async rating_IMBd() {
      http
        .post("/predict/", {
          votes: this.votes,
          duration: this.duration,
          budget_code: this.budget_code,
          rating: this.rating,
        })
        .then((response) => {
          this.precition_result = response.data.absolute_mean_error;
          this.rating_IMDb_result = response.data.rating_IMDb;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async recomendation_movie() {
      http
        .post("/recomendation/", {
          title: this.title,
        })
        .then((response) => {
          this.list_movie_r = response.data.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async list_movies() {
      http
        .get("/list_movies/")
        .then((response) => {
          //console.log(response.data.data)
          this.list_movies_str = response.data.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async movie_select() {
      this.votes = this.movie.Votes;
      this.duration = this.movie.Duration;
      this.budget_code = this.movie.budget_code;
      this.rating = this.movie.IMDb_Rating;
      this.rating_IMBd();
    },
    async movie_select_r() {
      //console.log(this.movie_r);
      this.title = this.movie_r.Title;
      this.recomendation_movie();
    },
  },
};
</script>
<style>
/* Helper classes */
.basil {
  background-color: #fffbe6 !important;
}
.basil--text {
  color: #356859 !important;
}
</style>