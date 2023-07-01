<template>
  <div>
    <div class="container section">
      <div class="row card-panel">
        <h4>
          <center>Ingresar archivos</center>
        </h4>
        <form class="col s12" @submit.prevent="SubirArchivos">
          <div class="file-field input-field">
            <div class="btn">
              <span>File</span>
              <input type="file" multiple />
            </div>
            <div class="file-path-wrapper">
              <input
                class="file-path validate"
                type="text"
                placeholder="Sube uno o más archivos"
              />
            </div>
          </div>
          <button
            class="btn waves-effect waves-green right"
            type="submit"
            name="enviar"
          >
            Enviar
            <i class="material-icons right">send</i>
          </button>
        </form>
      </div>
    </div>
    <div class="container section">
      <div class="row card-panel">
        <h4>
          <center>Ingresar consulta</center>
        </h4>
        <form class="col s12" @submit.prevent="Consulta_parser">
          <div class="row">
            <div class="input-field col s12">
              <i class="material-icons prefix">search</i>
              <input
                v-model="busqueda.busqueda_input"
                type="text"
                class="validate"
                required
              />
              <label for="Ingresa la categoria">Ingresa la busqueda</label>
            </div>
          </div>

          <div class="row">
            <div class="input-field col s12">
              <i class="material-icons prefix">clear_all</i>
              <input
                v-model="busqueda.top_k"
                type="text"
                class="validate"
                required
              />
              <label for="Ingresa la categoria">Ingresa el top K</label>
            </div>
          </div>

          <button
            class="btn waves-effect waves-green right"
            type="submit"
            name="enviar"
          >
            Enviar
            <i class="material-icons right">send</i>
          </button>
        </form>
      </div>
    </div>
    <div class="container section">
      <div class="row card-panel low-opacity">
        <div class="tables-wrapper">
          <table class="highlight centered">
            <thead>
              <tr>
                <th>Top k - Phyton</th>
                <!-- Agrega más columnas si es necesario -->
              </tr>
            </thead>
            <tbody>
              <!-- Itera sobre tabla1Data para generar las filas -->
              <tr v-for="item in tabla1Data" :key="item.id">
                <td>{{ item }}</td>
                <!-- Agrega más columnas si es necesario -->
              </tr>
            </tbody>
          </table>

          <table class="highlight centered">
            <thead>
              <tr>
                <th>Top k - Postgres/MongoDB</th>
                <!-- Agrega más columnas si es necesario -->
              </tr>
            </thead>
            <tbody>
              <!-- Itera sobre tabla2Data para generar las filas -->
              <tr v-for="item in tabla2Data" :key="item.id">
                <td>{{ item }}</td>
                <!-- Agrega más columnas si es necesario -->
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Services from "@/services/Services";
import Papa from "papaparse";

export default {
  name: "Category-manager",

  data() {
    return {
      post: {
        title: "",
        publication: "",
        author: "",
        date: "",
        year: "",
        month: "",
        content: "",
      },
      query: {
        stopword: "",
        idf: "",
      },
      busqueda: {
        busqueda_input: "",
        top_k: "",
      },
      datos_query: [],
      datos_post: [],
      datos: [],
    };
  },

  created() {
    this.getPosts();
  },
  methods: {
    getPosts() {
      Services.getPosts().then((response) => {
        this.datos = response.data.posts;
      });
    },
    SubirArchivos() {
      const files = document.querySelector('input[type="file"]').files;
      const file = files[0];

      Papa.parse(file, {
        header: true,
        complete: (results) => {
          const datos = results.data;
          this.datos_post = datos;

          const batchSize = 100; // Tamaño del lote
          const delay = 100; // Retardo entre cada lote (en milisegundos)

          let index = 0;

          const sendBatch = () => {
            for (let i = 0; i < batchSize && index < datos.length; i++) {
              this.post.title = this.datos_post[index].title;
              this.post.publication = this.datos_post[index].publication;
              this.post.author = this.datos_post[index].author;
              this.post.date = this.datos_post[index].date;
              this.post.year = this.datos_post[index].year;
              this.post.month = this.datos_post[index].month;
              this.post.content = this.datos_post[index].content;

              Services.postPost(this.post).then((response) => {
                this.datos = response.data.posts;
              });

              index++;
            }

            if (index < datos.length) {
              setTimeout(sendBatch, delay);
            }
          };

          sendBatch();
        },
      });
    },
    Consulta_parser() {
      Services.postParser(this.busqueda).then((response) => {
        this.datos_busqueda = response.data.busqueda;
      });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.title-bg {
  background-color: rgb(187, 182, 182); /* Color de fondo blanco */
  padding: 10px; /* Espaciado interno */
}

.tables-wrapper {
  display: flex;
  justify-content: space-between;
}

.row.card-panel.low-opacity {
  background-color: rgba(
    255,
    255,
    255,
    0.6
  ); /* Color de fondo con baja opacidad */
}
</style>
