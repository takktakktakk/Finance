document.addEventListener("DOMContentLoaded", function () {

    const beanInput = document.getElementById("bean_amount");
    const waterInput = document.getElementById("water_amount");
    const ratioInput = document.getElementById("ratio");

    function calculateRatio() {
        if (!beanInput || !waterInput || !ratioInput) return;

        const bean = parseFloat(beanInput.value);
        const water = parseFloat(waterInput.value);

        if (bean > 0 && water > 0) {
            const ratio = (water / bean).toFixed(1);
            ratioInput.value = "1 : " + ratio;
        } else {
            ratioInput.value = "";
        }
    }

    if (beanInput && waterInput) {
        beanInput.addEventListener("input", calculateRatio);
        waterInput.addEventListener("input", calculateRatio);

        calculateRatio(); // editページ対応
    }

});

// お気に入り切替
document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".favorite-btn").forEach(button => {

        button.addEventListener("click", function () {

            // 🔒 すでに通信中なら無視
            if (this.dataset.loading === "true") {
                return;
            }

            const recipeId = this.dataset.id;

            // 🔒 ロック開始
            this.dataset.loading = "true";
            this.disabled = true;

            fetch(`/toggle_favorite/${recipeId}`, {
                method: "POST"
            })
                .then(res => res.json())
                .then(data => {

                    const icon = this.querySelector("i");

                    // 状態切替
                    this.classList.toggle("active");

                    if (this.classList.contains("active")) {
                        icon.classList.remove("bi-heart");
                        icon.classList.add("bi-heart-fill");
                    } else {
                        icon.classList.remove("bi-heart-fill");
                        icon.classList.add("bi-heart");
                    }

                    // アニメーション
                    this.classList.add("animate");

                    setTimeout(() => {
                        this.classList.remove("animate");
                    }, 350);
                })
                .catch(err => {
                    console.error("Error:", err);
                })
                .finally(() => {
                    // 🔓 ロック解除
                    this.dataset.loading = "false";
                    this.disabled = false;
                });
        });

    });

});