/**
 * CourseManager.js
 * Gestión de progreso de lecciones e interactividad LMS en cliente (localStorage).
 */

export class CourseManager {
    constructor() {
        this.layout = document.querySelector('.c-lesson-layout');
        if (!this.layout) return;

        this.courseId = this.layout.getAttribute('data-config-course-id');
        this.storageKey = `datamaq_course_${this.courseId}_progress`;

        this.markBtn = document.getElementById('mark-complete-btn');
        this.progressFill = document.getElementById('course-progress-fill');
        this.progressText = document.getElementById('course-progress-text');
        this.sidebarLessons = document.querySelectorAll('.c-lesson-sidebar-lesson-item');
        
        // Elementos del sidebar móvil
        this.sidebar = document.getElementById('lesson-sidebar');
        this.sidebarBackdrop = document.getElementById('sidebar-backdrop');
        this.toggleSidebarBtn = document.getElementById('toggle-sidebar-btn');
        this.closeSidebarBtn = document.getElementById('close-sidebar-btn');

        this.completedLessons = this.loadProgress();
        this.init();
    }

    init() {
        // Inicializar barra lateral móvil
        if (this.sidebar && this.toggleSidebarBtn) {
            this.toggleSidebarBtn.addEventListener('click', () => this.openSidebar());
        }
        if (this.closeSidebarBtn) {
            this.closeSidebarBtn.addEventListener('click', () => this.closeSidebar());
        }
        if (this.sidebarBackdrop) {
            this.sidebarBackdrop.addEventListener('click', () => this.closeSidebar());
        }

        // Inicializar clases de completado en el sidebar según el localStorage
        this.sidebarLessons.forEach(item => {
            const lessonId = item.getAttribute('data-lesson-id');
            if (this.completedLessons.includes(lessonId)) {
                item.classList.add('is-completed');
            }
        });

        // Inicializar el botón de marcar completado para la lección actual
        if (this.markBtn) {
            const currentLessonId = this.markBtn.getAttribute('data-lesson-id');
            if (this.completedLessons.includes(currentLessonId)) {
                this.markBtn.classList.add('is-completed');
            }

            this.markBtn.addEventListener('click', () => {
                this.toggleLessonComplete(currentLessonId);
            });
        }

        // Inicializar lógica de cuestionario interactivo
        this.initQuiz();

        // Actualizar porcentaje y barra de progreso al cargar
        this.updateProgressBar();
    }

    /**
     * Inicializa los manejadores de eventos para los cuestionarios (quizzes).
     */
    initQuiz() {
        const quizContainer = document.getElementById('quiz-container');
        if (!quizContainer) return;

        const submitBtn = document.getElementById('quiz-submit-btn');
        const resetBtn = document.getElementById('quiz-reset-btn');
        const form = document.getElementById('quiz-form');
        const resultContainer = document.getElementById('quiz-result');
        const resultScore = document.getElementById('quiz-result-score');
        const questionCards = quizContainer.querySelectorAll('.c-quiz-question-card');

        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                // Verificar que se hayan respondido todas las preguntas
                const allAnswered = Array.from(questionCards).every(card => {
                    const questionId = card.getAttribute('data-question-id');
                    const checked = form.querySelector(`input[name="question_${questionId}"]:checked`);
                    return checked !== null;
                });

                if (!allAnswered) {
                    alert('Por favor, responde todas las preguntas antes de verificar.');
                    return;
                }

                let correctAnswersCount = 0;

                questionCards.forEach(card => {
                    const questionId = card.getAttribute('data-question-id');
                    const correctOption = parseInt(card.getAttribute('data-correct-option'), 10);
                    const selectedInput = form.querySelector(`input[name="question_${questionId}"]:checked`);
                    const selectedValue = parseInt(selectedInput.value, 10);
                    
                    const feedbackContainer = document.getElementById(`feedback_${questionId}`);
                    const badgeCorrect = feedbackContainer.querySelector('.feedback-badge-correct');
                    const badgeIncorrect = feedbackContainer.querySelector('.feedback-badge-incorrect');
                    
                    // Mostrar feedback
                    feedbackContainer.style.display = 'block';
                    if (selectedValue === correctOption) {
                        correctAnswersCount++;
                        badgeCorrect.style.display = 'inline-flex';
                        badgeIncorrect.style.display = 'none';
                    } else {
                        badgeCorrect.style.display = 'none';
                        badgeIncorrect.style.display = 'inline-flex';
                    }

                    // Deshabilitar opciones
                    const inputs = form.querySelectorAll(`input[name="question_${questionId}"]`);
                    inputs.forEach(input => input.disabled = true);
                });

                // Calcular e imprimir resultado
                const scorePercentage = Math.round((correctAnswersCount / questionCards.length) * 100);
                if (resultScore) {
                    resultScore.textContent = `Obtuviste ${scorePercentage}% (${correctAnswersCount} de ${questionCards.length} correctas)`;
                }
                if (resultContainer) {
                    resultContainer.style.display = 'block';
                }

                submitBtn.style.display = 'none';
                if (resetBtn) resetBtn.style.display = 'inline-flex';
                
                // Opcional: Marcar automáticamente la lección (quiz) como completada al verificarla
                const currentLessonId = this.markBtn ? this.markBtn.getAttribute('data-lesson-id') : null;
                if (currentLessonId && !this.completedLessons.includes(currentLessonId)) {
                    this.toggleLessonComplete(currentLessonId);
                }
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                // Habilitar y desmarcar opciones
                questionCards.forEach(card => {
                    const questionId = card.getAttribute('data-question-id');
                    const inputs = form.querySelectorAll(`input[name="question_${questionId}"]`);
                    inputs.forEach(input => {
                        input.disabled = false;
                        input.checked = false;
                    });

                    const feedbackContainer = document.getElementById(`feedback_${questionId}`);
                    if (feedbackContainer) {
                        feedbackContainer.style.display = 'none';
                    }
                });

                if (resultContainer) {
                    resultContainer.style.display = 'none';
                }

                resetBtn.style.display = 'none';
                if (submitBtn) submitBtn.style.display = 'inline-flex';
            });
        }
    }

    /**
     * Carga la lista de IDs de lecciones completadas desde localStorage.
     */
    loadProgress() {
        try {
            const data = localStorage.getItem(this.storageKey);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            console.error('[CourseManager] Error cargando progreso:', e);
            return [];
        }
    }

    /**
     * Guarda la lista de IDs de lecciones completadas en localStorage.
     */
    saveProgress() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.completedLessons));
        } catch (e) {
            console.error('[CourseManager] Error guardando progreso:', e);
        }
    }

    /**
     * Marca o desmarca una lección como completada.
     * @param {string} lessonId
     */
    toggleLessonComplete(lessonId) {
        const index = this.completedLessons.indexOf(lessonId);
        let completed = false;

        if (index === -1) {
            this.completedLessons.push(lessonId);
            completed = true;
        } else {
            this.completedLessons.splice(index, 1);
        }

        this.saveProgress();

        // Actualizar el estado del botón en la interfaz
        if (this.markBtn && this.markBtn.getAttribute('data-lesson-id') === lessonId) {
            if (completed) {
                this.markBtn.classList.add('is-completed');
            } else {
                this.markBtn.classList.remove('is-completed');
            }
        }

        // Actualizar el item del sidebar correspondiente
        const sidebarItem = document.querySelector(`.c-lesson-sidebar-lesson-item[data-lesson-id="${lessonId}"]`);
        if (sidebarItem) {
            if (completed) {
                sidebarItem.classList.add('is-completed');
            } else {
                sidebarItem.classList.remove('is-completed');
            }
        }

        // Actualizar barra de progreso global
        this.updateProgressBar();
    }

    /**
     * Calcula y actualiza la barra de progreso y el texto de porcentaje.
     */
    updateProgressBar() {
        const totalLessonsCount = this.sidebarLessons.length;
        if (totalLessonsCount === 0) return;

        const completedCount = this.completedLessons.length;
        const percentage = Math.round((completedCount / totalLessonsCount) * 100);

        if (this.progressFill) {
            this.progressFill.style.width = `${percentage}%`;
        }

        if (this.progressText) {
            this.progressText.textContent = `${percentage}% completado`;
    }

    openSidebar() {
        if (this.sidebar) this.sidebar.classList.add('is-open');
        if (this.sidebarBackdrop) this.sidebarBackdrop.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    }

    closeSidebar() {
        if (this.sidebar) this.sidebar.classList.remove('is-open');
        if (this.sidebarBackdrop) this.sidebarBackdrop.classList.remove('is-open');
        document.body.style.overflow = '';
    }
}

// Inicialización automática
document.addEventListener('DOMContentLoaded', () => {
    new CourseManager();
});
