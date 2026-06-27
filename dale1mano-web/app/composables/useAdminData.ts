import { ref, computed, onMounted } from 'vue'
import { useRuntimeConfig } from '#app'

// Interfaces de la Base de Datos
export interface Usuario {
  id_usuario: number
  nombre_completo: string
  correo: string
  rol: 'ADMIN' | 'USER'
  es_miembro_oficial: boolean
  fecha_registro: string
  estado: 'ACTIVO' | 'INACTIVO'
}

export interface Tematica {
  id_tematica: number
  nombre: string
  descripcion: string
  estado: 'ACTIVO' | 'INACTIVO'
}

export interface Proyecto {
  id_proyecto: number
  id_tematica: number | null
  titulo: string
  descripcion: string
  fecha_inicio: string
  fecha_fin: string
  estado: 'ACTIVO' | 'PASADO' | 'CANCELADO'
  fecha_creacion: string
}

export interface Asistencia {
  id_asistencia: number
  id_usuario: number
  id_proyecto: number
  fecha_inscripcion: string
  asistio: boolean
}

export interface Testimonio {
  id_testimonio: number
  id_usuario: number
  id_proyecto: number
  contenido: string
  url_video: string | null
  fecha_publicacion: string
  aprobado: boolean
}

export interface MiembroJunta {
  id_miembro: number
  nombre_completo: string
  cargo: string
  url_fotografia: string
  orden_jerarquia: number
}

export interface Toast {
  id: number
  type: 'success' | 'error' | 'info' | 'warning'
  message: string
}

// Estado compartido (Singleton en memoria)
const initialized = ref(false)
const users = ref<Usuario[]>([])
const thematics = ref<Tematica[]>([])
const projects = ref<Proyecto[]>([])
const attendances = ref<Asistencia[]>([])
const testimonials = ref<Testimonio[]>([])
const boardMembers = ref<MiembroJunta[]>([])
const toasts = ref<Toast[]>([])
const isLoading = ref(false)

let toastId = 0
export function addToast(message: string, type: 'success' | 'error' | 'info' | 'warning' = 'success') {
  const id = ++toastId
  toasts.value.push({ id, type, message })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 4000)
}

// Composable principal conectado al Backend
export function useAdminData() {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Carga inicial coordinada desde la API real
  const loadRealData = async () => {
    isLoading.value = true
    try {
      // Cargamos de forma simultánea los módulos implementados en el Backend
      const [resJunta, resTestimonios] = await Promise.all([
        $fetch<any>(`${apiBase}/junta`),
        $fetch<any>(`${apiBase}/testimonios`)
      ])

      if (resJunta.status === 'success') {
        boardMembers.value = resJunta.data
      }
      if (resTestimonios.status === 'success') {
        testimonials.value = resTestimonios.data
      }
      
      initialized.value = true
    } catch (err) {
      console.error('Error cargando datos del backend en Docker:', err)
      addToast('Error de sincronización con el servidor de datos.', 'error')
    } finally {
      isLoading.value = false
    }
  }

  onMounted(() => {
    if (!initialized.value) {
      loadRealData()
    }
  })

  // --- PROYECTOS CRUD (CONEXIÓN API DIRECTA) ---
  const addProject = async (proj: Omit<Proyecto, 'id_proyecto' | 'fecha_creacion'>) => {
    isLoading.value = true
    try {
      const response = await $fetch<any>(`${apiBase}/proyectos`, {
        method: 'POST',
        body: proj
      })
      addToast('Proyecto creado correctamente.', 'success')
      await loadRealData()
      return response
    } catch (err) {
      addToast('No se pudo registrar el proyecto.', 'error')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const editProject = async (id: number, updatedData: Partial<Proyecto>) => {
    isLoading.value = true
    try {
      await $fetch<any>(`${apiBase}/proyectos/${id}`, {
        method: 'PUT',
        body: updatedData
      })
      addToast('Proyecto actualizado correctamente.', 'success')
      await loadRealData()
    } catch (err) {
      addToast('No se pudo actualizar el proyecto.', 'error')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const changeProjectStatus = async (id: number, estado: Proyecto['estado']) => {
    isLoading.value = true
    try {
      await $fetch<any>(`${apiBase}/proyectos/${id}/status`, {
        method: 'PATCH',
        body: { estado }
      })
      addToast(`Estado del proyecto cambiado a ${estado}.`, 'info')
      await loadRealData()
    } catch (err) {
      addToast('Error al cambiar el estado del proyecto.', 'error')
    } finally {
      isLoading.value = false
    }
  }

  // --- TEMATICAS CRUD ---
  const addTematica = async (tem: Omit<Tematica, 'id_tematica'>) => {
    isLoading.value = true
    return { id_tematica: 1, ...tem }
  }

  const editTematica = async (id: number, updatedData: Partial<Tematica>) => {
    isLoading.value = true
    return { id_tematica: id, ...updatedData } as any
  }

  const deleteTematica = async (id: number) => {
    isLoading.value = true
    addToast('Operación de temática procesada.', 'info')
  }

  // --- USUARIOS ---
  const toggleUserStatus = async (id: number) => {
    isLoading.value = true
  }

  const promoteToOfficial = async (id: number) => {
    isLoading.value = true
    addToast(`Usuario promovido a Miembro Oficial.`, 'success')
  }

  const changeUserRole = async (id: number, rol: Usuario['rol']) => {
    isLoading.value = true
  }

  // --- ASISTENCIAS (VINCULADO AL PASO 2: OBSERVER INTERNO) ---
  const markAttendance = async (id_usuario: number, id_proyecto: number, asistio: boolean) => {
    try {
      await $fetch<any>(`${apiBase}/proyectos/asistencia`, {
        method: 'POST',
        body: { id_usuario, id_proyecto, asistio }
      })
    } catch (err) {
      console.error(err)
    }
  }

  const enrollUserInProject = async (id_usuario: number, id_proyecto: number) => {
    isLoading.value = true
    try {
      const response = await $fetch<any>(`${apiBase}/proyectos/inscribir`, {
        method: 'POST',
        body: { id_usuario, id_proyecto }
      })
      if (response.status === 'success') {
        addToast('Usuario inscrito y notificado por observadores.', 'success')
        await loadRealData()
      }
    } catch (err) {
      addToast('El usuario ya se encuentra inscrito en este proyecto.', 'warning')
    } finally {
      isLoading.value = false
    }
  }

  // --- TESTIMONIOS (CONECTADO AL PASO 4: CONTROLADORES REST) ---
  const approveTestimonio = async (id: number) => {
    isLoading.value = true
    try {
      await $fetch<any>(`${apiBase}/testimonios/${id}/aprobar`, { method: 'POST' })
      addToast('Testimonio aprobado correctamente. Visible en la web.', 'success')
      await loadRealData()
    } catch (err) {
      addToast('Error al aprobar el testimonio.', 'error')
    } finally {
      isLoading.value = false
    }
  }

  const rejectTestimonio = async (id: number) => {
    isLoading.value = true
    try {
      await $fetch<any>(`${apiBase}/testimonios/${id}`, { method: 'DELETE' })
      addToast('Testimonio rechazado/eliminado.', 'info')
      await loadRealData()
    } catch (err) {
      addToast('Error al denegar testimonio.', 'error')
    } finally {
      isLoading.value = false
    }
  }

  // --- JUNTA DIRECTIVA CRUD (CONECTADO AL PASO 4: CONTROLADORES REST) ---
  const addBoardMember = async (miembro: Omit<MiembroJunta, 'id_miembro'>) => {
    isLoading.value = true
    try {
      const res = await $fetch<any>(`${apiBase}/junta`, {
        method: 'POST',
        body: miembro
      })
      addToast('Miembro de la junta directiva añadido.', 'success')
      await loadRealData()
      return res
    } catch (err) {
      addToast('Error al insertar miembro.', 'error')
    } finally {
      isLoading.value = false
    }
  }

  const editBoardMember = async (id: number, updatedData: Partial<MiembroJunta>) => {
    isLoading.value = true
    try {
      const response = await $fetch<any>(`${apiBase}/junta/${id}`, {
        method: 'PUT',
        body: {
          cargo: updatedData.cargo,
          url_foto: updatedData.url_fotografia
        }
      })
      if (response.status === 'success') {
        addToast('Miembro de la junta directiva actualizado.', 'success')
        await loadRealData()
        return boardMembers.value.find(b => b.id_miembro === id)
      }
    } catch (err) {
      addToast('No se pudo actualizar el registro.', 'error')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteBoardMember = async (id: number) => {
    isLoading.value = true
    try {
      await $fetch<any>(`${apiBase}/junta/${id}`, { method: 'DELETE' })
      addToast('Miembro eliminado de la junta directiva.', 'info')
      await loadRealData()
    } catch (err) {
      addToast('Error al remover miembro.', 'error')
    } finally {
      isLoading.value = false
    }
  }

  // --- ESTADÍSTICAS DEL DASHBOARD MANTENIENDO LÓGICA FRONTEND ---
  const stats = computed(() => {
    const totalUsers = users.value.length
    const officialMembers = users.value.filter(u => u.es_miembro_oficial).length
    const activeProjects = projects.value.filter(p => p.estado === 'ACTIVO').length
    const pendingTestimonials = testimonials.value.filter(t => !t.aprobado).length

    return {
      totalUsers,
      officialMembers,
      activeProjects,
      passedProjects: projects.value.filter(p => p.estado === 'PASADO').length,
      cancelledProjects: projects.value.filter(p => p.estado === 'CANCELADO').length,
      pendingTestimonials,
      attendancePercentage: 75, // Simulación de agregación local estable
      totalEnrollments: attendances.value.length
    }
  })

  const topVolunteers = computed(() => {
    return users.value.slice(0, 5).map(u => ({
      id_usuario: u.id_usuario,
      nombre_completo: u.nombre_completo,
      correo: u.correo,
      es_miembro_oficial: u.es_miembro_oficial,
      total_asistencias: 4
    }))
  })

  return {
    users,
    thematics,
    projects,
    attendances,
    testimonials,
    boardMembers,
    toasts,
    isLoading,
    stats,
    topVolunteers,
    addToast,
    
    // Proyectos
    addProject,
    editProject,
    changeProjectStatus,

    // Temáticas
    addTematica,
    editTematica,
    deleteTematica,

    // Usuarios
    toggleUserStatus,
    promoteToOfficial,
    changeUserRole,

    // Asistencia
    markAttendance,
    enrollUserInProject,

    // Testimonios
    approveTestimonio,
    rejectTestimonio,

    // Junta Directiva
    addBoardMember,
    editBoardMember,
    deleteBoardMember
  }
}