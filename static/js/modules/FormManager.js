export class FormManager {
    constructor(formElement, apiUrl) {
        this.form = formElement;
        this.apiUrl = apiUrl;
        this.steps = Array.from(this.form.querySelectorAll('.c-contact__step-panel'));
        this.currentStep = 0;
        this.init();
    }

    init() {
        this.form.querySelector('.c-contact__actions button').addEventListener('click', () => this.handleNextOrSubmit());
    }

    handleNextOrSubmit() {
        if (this.currentStep < this.steps.length - 1) {
            this.showStep(this.currentStep + 1);
        } else {
            this.submitForm();
        }
    }

    showStep(index) {
        this.steps[this.currentStep].style.display = 'none';
        this.steps[index].style.display = 'block';
        this.currentStep = index;
    }

    collectData() {
        const getVal = (id) => this.form.querySelector('#' + id)?.value || '';

        const data = {
            name: `${getVal('contacto-nombre')} ${getVal('contacto-apellido')}`.trim(),
            comment: getVal('contacto-comentario'),
            email: getVal('contacto-email'),
            phone: getVal('contacto-telefono'),
            createdAt: new Date().toISOString(),
            pageLocation: window.location.href
        };
        return data;
    }

    async submitForm() {
        const payload = this.collectData();
        console.debug('Enviando payload:', payload);

        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                console.info('Formulario enviado con éxito.');
                this.form.innerHTML = '<p class="tw:text-green-500">¡Gracias! Tu consulta ha sido recibida correctamente.</p>';

                // GA4: evento de conversión (solo si hay consentimiento de cookies)
                if (window.dataLayer && typeof window.dataLayer.push === 'function') {
                    window.dataLayer.push({
                        event: 'generate_lead',
                        lead_source: 'formulario_contacto'
                    });
                }

                // Google Ads: evento de conversión (requiere GOOGLE_ADS_CONVERSION_ID en consola)
                if (window.APP_CONFIG?.googleAdsConversionId
                    && window.APP_CONFIG.googleAdsConversionId !== "None"
                    && typeof window.gtag === 'function') {
                    window.gtag('event', 'conversion', {
                        send_to: window.APP_CONFIG.googleAdsConversionId
                    });
                }
            } else {
                throw new Error(`Error del servidor: ${response.status}`);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}