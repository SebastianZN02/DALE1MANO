<template>
  <div class="min-h-screen flex flex-col bg-gray-50 text-gray-800">
    <LayoutNavbar @openLogin="handleOpenLogin" />

    <main class="flex-grow">
      <slot />
    </main>

    <LayoutFooter />
		<LoginModal 
      :isOpen="isLoginModalOpen" 
      @close="isLoginModalOpen = false" 
      @loginSuccess="handleLoginSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Estado para controlar la apertura del modal
const isLoginModalOpen = ref(false)

function handleLoginSuccess(adminData: { adminId: number; nombre: string; rol: string }) {
  isLoginModalOpen.value = false
  
  // Redirección hacia administración solo si es un rol ADMIN
  if (adminData.rol === 'ADMIN') {
    navigateTo('/admin') 
  } else {
    // Si es un voluntario común (USER), lo dejamos en la página principal
    navigateTo('/')
  }
}

function handleOpenLogin() {
  console.log('Layout: openLogin event received. Opening modal...')
  isLoginModalOpen.value = true
}
</script>

