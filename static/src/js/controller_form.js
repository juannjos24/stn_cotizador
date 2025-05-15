/** @odoo-module **/

console.log("🟢 [brand_selector.js] Script cargado correctamente");

setTimeout(() => {
    const imageButtons = document.querySelectorAll("[data-brand-id]");
    const selectBrand = document.querySelector("select[name='brand_id']");
    const selectModel = document.querySelector("select[name='model_id']");
    const selectYear = document.querySelector("select[name='year_id']");
    const selectVersion = document.querySelector("select[name='version_id']");

    const clearAndInit = (select, placeholder) => {
        if (select) select.innerHTML = `<option value="">${placeholder}</option>`;
    };

    const fetchData = async (url, payload) => {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
    
        const json = await response.json();
        if (!Array.isArray(json.result)) {
            console.error("❌ La propiedad `result` no es una lista:", json);
            return [];
        }
        return json.result;  // ✅ aquí sí accedes correctamente
    };
    
    const loadModels = async (brandId) => {
        console.log("🔄 Solicitando modelos para brand_id=" + brandId);
        const models = await fetchData('/api/models', { brand_id: brandId });
        clearAndInit(selectModel, "Selecciona un modelo");
        clearAndInit(selectYear, "Selecciona un año");
        clearAndInit(selectVersion, "Selecciona una versión");
        console.log("📥 Modelos recibidos:", models);
        models.forEach(m => {
            const opt = new Option(m.name, m.id);
            selectModel.appendChild(opt);
        });
    };

    const loadYear = async (modelId) => {
        console.log("🔄 Solicitando año para model_id=" + modelId);
        const years = await fetchData('/api/years', { model_id: modelId });
        clearAndInit(selectYear, "Selecciona un año");
        clearAndInit(selectVersion, "Selecciona una versión");
        years.forEach(y => {
            const opt = new Option(y.name, y.id);
            selectYear.appendChild(opt);
        });
    };

    const loadVersions = async (modelId) => {
        console.log("🔄 Solicitando versiones para model_id=" + modelId);
        const versions = await fetchData('/api/versions', { model_id: modelId });
        clearAndInit(selectVersion, "Selecciona una versión");
        versions.forEach(v => {
            const opt = new Option(v.name, v.id);
            selectVersion.appendChild(opt);
        });
    };

    // Cambios manuales en el selector de marca
    if (selectBrand) {
        selectBrand.addEventListener("change", (e) => {
            const brandId = e.target.value;
            if (brandId) loadModels(brandId);
        });
    }

    // Cambios en modelo → actualiza año y versiones
    if (selectModel) {
        selectModel.addEventListener("change", (e) => {
            const modelId = e.target.value;
            if (modelId) {
                loadYear(modelId);
                loadVersions(modelId);
            }
        });
    }

    // Soporte para clic en imágenes
    imageButtons.forEach((img) => {
        img.addEventListener("click", () => {
            const brandId = img.dataset.brandId;
            if (brandId) {
                console.log(`🖱️ Imagen clickeada: brand_id=${brandId}`);
                selectBrand.value = brandId;
                selectBrand.dispatchEvent(new Event("change"));
            }
        });
    });
}, 500);
