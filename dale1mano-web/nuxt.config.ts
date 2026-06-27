// https://nuxt.com/docs/api/configuration/nuxt-config

declare const process: {
  env: {
    NUXT_PUBLIC_API_BASE?: string
    [key: string]: string | undefined
  }
}

export default defineNuxtConfig({
  // Compatibilidad de versión
  compatibilityDate: '2024-04-03',
  
  // Habilita las herramientas de desarrollo en el navegador
  devtools: { enabled: true },

  // Si estás utilizando Tailwind CSS u otros módulos, asegúrate de mantenerlos aquí.
  // Ejemplo: modules: ['@nuxtjs/tailwindcss'],

  // Configuración de variables de entorno (Clave para Docker)
  runtimeConfig: {
    public: {
      // Si la variable NUXT_PUBLIC_API_BASE existe en Docker, la usa.
      // Si no, por defecto apunta al localhost para desarrollo.
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:5000/api'
    }
  }
})