
        // Smooth scroll for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });

        // Add scroll animation to elements
        const scrollElements = document.querySelectorAll('.scroll-fade');

        const elementInView = (el, dividend = 1) => {
            const elementTop = el.getBoundingClientRect().top;
            return (
                elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
            );
        };

        const displayScrollElement = (element) => {
            element.classList.add('visible');
        };

        const handleScrollAnimation = () => {
            scrollElements.forEach((el) => {
                if (elementInView(el, 1.25)) {
                    displayScrollElement(el);
                }
            });
        };

        window.addEventListener('scroll', () => {
            handleScrollAnimation();
        });

        // Copy bank account number to clipboard
        const copyBtn = document.querySelector('.copy-btn');
        if (copyBtn) {
            copyBtn.addEventListener('click', function() {
                const accountNumber = '106537259839';
                navigator.clipboard.writeText(accountNumber).then(() => {
                    alert('Nomor rekening Bank Jago berhasil disalin: 1065 3725 9839 (a.n. Asep Safrudin)');
                }).catch(err => {
                    console.error('Gagal menyalin: ', err);
                });
            });
        }

        // Gallery Slideshow
        document.addEventListener('DOMContentLoaded', () => {
            const slides = document.querySelectorAll('.gallery-slide');
            const prevBtn = document.querySelector('.gallery-prev');
            const nextBtn = document.querySelector('.gallery-next');
            let currentSlide = 0;

            function showSlide(n) {
                if (slides.length === 0) return;
                slides.forEach(slide => slide.classList.remove('active'));
                slides[n].classList.add('active');
            }

            function nextSlide() {
                if (slides.length === 0) return;
                currentSlide = (currentSlide + 1) % slides.length;
                showSlide(currentSlide);
            }

            function prevSlide() {
                if (slides.length === 0) return;
                currentSlide = (currentSlide - 1 + slides.length) % slides.length;
                showSlide(currentSlide);
            }

            if(slides.length > 0) {
                showSlide(currentSlide);
                prevBtn.addEventListener('click', prevSlide);
                nextBtn.addEventListener('click', nextSlide);

                // Optional: Auto-play, uncomment the line below
                // setInterval(nextSlide, 5000); 
            }
        });

        // =========================================================================
        // Hidrasi Data Keuangan RT Dinamis (Sumber Kanonik Database GHS Keuangan)
        // =========================================================================
        (function() {
            function formatRupiah(num) {
                if (num === null || num === undefined || isNaN(num)) return 'Rp0';
                var val = Math.round(Number(num));
                return 'Rp' + val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
            }

            function formatTanggalIndo(strDate) {
                if (!strDate) return '-';
                var parts = strDate.split('-');
                if (parts.length < 3) return strDate;
                var bulanMap = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
                var idx = parseInt(parts[1], 10) - 1;
                return parts[2] + ' ' + (bulanMap[idx] || parts[1]) + ' ' + parts[0];
            }

            function renderFinanceSection(data) {
                if (!data) return;

                // 1. Update Badge Waktu
                var updateTextEl = document.getElementById('finance-update-text');
                if (updateTextEl && data.updated_at) {
                    updateTextEl.textContent = 'Update: ' + data.updated_at;
                }

                // 2. Update 4 Metrik Utama
                var saldoEl = document.getElementById('stat-saldo-kas');
                if (saldoEl && data.saldo_kas !== undefined) {
                    saldoEl.textContent = formatRupiah(data.saldo_kas);
                }

                var saldoSubEl = document.getElementById('stat-saldo-sub');
                if (saldoSubEl) {
                    var cash = (data.saldo_cash !== undefined) ? data.saldo_cash : data.saldo_kas;
                    var digital = data.saldo_digital || 0;
                    saldoSubEl.textContent = '💵 Tunai: ' + formatRupiah(cash) + ' | 💳 Bank Jago: ' + formatRupiah(digital);
                }

                var masukEl = document.getElementById('stat-total-masuk');
                if (masukEl && data.total_pemasukan !== undefined) {
                    masukEl.textContent = formatRupiah(data.total_pemasukan);
                }

                var subMasukEl = document.getElementById('stat-sub-masuk');
                if (subMasukEl && data.count_pemasukan !== undefined) {
                    subMasukEl.textContent = data.count_pemasukan + ' transaksi setoran iuran warga';
                }

                var keluarEl = document.getElementById('stat-total-keluar');
                if (keluarEl && data.total_pengeluaran !== undefined) {
                    keluarEl.textContent = formatRupiah(data.total_pengeluaran);
                }

                var subKeluarEl = document.getElementById('stat-sub-keluar');
                if (subKeluarEl && data.count_pengeluaran !== undefined) {
                    subKeluarEl.textContent = data.count_pengeluaran + ' mutasi realisasi anggaran RT';
                }

                var wargaCountEl = document.getElementById('stat-warga-count');
                var wargaSubEl = document.getElementById('stat-warga-sub');
                if (data.warga) {
                    if (wargaCountEl) wargaCountEl.textContent = (data.warga.dihuni || 62) + ' / ' + (data.warga.total || 73);
                    if (wargaSubEl) wargaSubEl.textContent = (data.warga.dihuni || 62) + ' Rumah Dihuni, ' + (data.warga.kosong || 11) + ' Kavling Kosong';
                }

                // 3. Update Breakdown Kategori Pengeluaran
                var headerBelanja = document.getElementById('finance-total-belanja-header');
                if (headerBelanja && data.total_pengeluaran !== undefined) {
                    headerBelanja.textContent = 'Total: ' + formatRupiah(data.total_pengeluaran);
                }

                var catContainer = document.getElementById('finance-categories-container');
                if (catContainer && Array.isArray(data.kategori_pengeluaran) && data.kategori_pengeluaran.length > 0) {
                    var totalExpense = data.total_pengeluaran || 1;
                    var catHtml = '';
                    data.kategori_pengeluaran.forEach(function(item) {
                        var percent = ((item.total / totalExpense) * 100).toFixed(1);
                        catHtml += '<div class="cat-progress-item">' +
                            '<div class="cat-header">' +
                            '<span class="cat-name">' + item.kategori + '</span>' +
                            '<span class="cat-amount">' + formatRupiah(item.total) + ' (' + percent + '%)</span>' +
                            '</div>' +
                            '<div class="progress-track"><div class="progress-fill" style="width: ' + percent + '%;"></div></div>' +
                            '</div>';
                    });
                    catContainer.innerHTML = catHtml;
                }

                // 4. Update 8 Transaksi Terakhir
                var tbody = document.getElementById('finance-tx-tbody');
                if (tbody && Array.isArray(data.transaksi_terbaru) && data.transaksi_terbaru.length > 0) {
                    var txHtml = '';
                    var txSlice = data.transaksi_terbaru.slice(0, 8);
                    txSlice.forEach(function(tx) {
                        var isKeluar = (tx.jenis === 'Pengeluaran');
                        var badgeClass = isKeluar ? 'tx-badge-keluar' : 'tx-badge-masuk';
                        var nominalColor = isKeluar ? '#c62828' : '#1b5e20';
                        var prefix = isKeluar ? '-' : '+';
                        var uraianText = tx.uraian || tx.kategori || 'Transaksi Kas';
                        if (tx.nama_warga && tx.nama_warga !== 'Petugas Keamanan' && tx.nama_warga !== 'Petugas Kebersihan') {
                            if (!uraianText.toUpperCase().includes(tx.nama_warga.toUpperCase())) {
                                uraianText += ' (' + tx.nama_warga + ')';
                            }
                        }
                        var metode = tx.metode_kas ? (' ' + tx.metode_kas) : '';

                        txHtml += '<tr>' +
                            '<td>' + formatTanggalIndo(tx.tanggal) + '</td>' +
                            '<td>' + uraianText + '<br><span class="tx-badge ' + badgeClass + '">' + tx.jenis + metode + '</span></td>' +
                            '<td style="color: ' + nominalColor + '; font-weight: 700;">' + prefix + formatRupiah(tx.nominal) + '</td>' +
                            '</tr>';
                    });
                    tbody.innerHTML = txHtml;
                }

                // 5. Update Link Portal jika ada URL aktif
                if (data.portal_url) {
                    var portalLinks = document.querySelectorAll('.live-portal-link');
                    portalLinks.forEach(function(link) {
                        link.href = data.portal_url;
                    });
                }
            }

            // Inisialisasi: Render langsung dari finance_data.js (sinkron/cepat)
            if (window.GHS_FINANCE_DATA) {
                renderFinanceSection(window.GHS_FINANCE_DATA);
            }

            // Lakukan polling/fetch asinkron data terbaru dari JSON
            document.addEventListener('DOMContentLoaded', function() {
                if (window.GHS_FINANCE_DATA) {
                    renderFinanceSection(window.GHS_FINANCE_DATA);
                }
                fetch('data/finance_summary.json?v=' + Date.now())
                    .then(function(res) {
                        if (!res.ok) throw new Error('HTTP ' + res.status);
                        return res.json();
                    })
                    .then(function(data) {
                        renderFinanceSection(data);
                    })
                    .catch(function(err) {
                        // Fallback aman ke window.GHS_FINANCE_DATA
                        if (window.GHS_FINANCE_DATA) {
                            renderFinanceSection(window.GHS_FINANCE_DATA);
                        }
                    });
            });
        })();
