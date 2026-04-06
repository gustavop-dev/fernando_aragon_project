import { Swiper, SwiperSlide } from "swiper/react";
import { Autoplay, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";

import cert1 from "../../assets/certificates/Imagen1.png";
import cert2 from "../../assets/certificates/Imagen2.png";
import cert3 from "../../assets/certificates/Imagen3.png";
import cert4 from "../../assets/certificates/Imagen4.png";
import cert5 from "../../assets/certificates/Imagen5.png";
import cert6 from "../../assets/certificates/Imagen6.png";

const certificates = [
  { src: cert1, alt: "CELAC ISO 9001 - No. 10.016-5" },
  { src: cert2, alt: "CELAC NTC 5555 - No. 20.016-5" },
  { src: cert3, alt: "CELAC NTC 5581 - No. 30.051-5" },
  { src: cert4, alt: "CELAC NTC 5581 - No. 30.052-5" },
  { src: cert5, alt: "CELAC NTC 5581 - No. 30.053-5" },
  { src: cert6, alt: "CELAC NTC 5666 - No. 30.054-5" },
];

export default function CelacCertificates() {
  return (
    <section className="py-16 bg-[#f8f8fc]">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-10">
          <div className="flex items-center justify-center gap-3 mb-4">
            <span className="w-10 h-[2px] bg-[#F9B233]" />
            <span
              className="text-[#F9B233] text-[12px] tracking-[0.2em] uppercase"
              style={{ fontWeight: 700 }}
            >
              Calidad Certificada
            </span>
            <span className="w-10 h-[2px] bg-[#F9B233]" />
          </div>
          <h2
            className="text-[#29235C] text-[clamp(1.8rem,3vw,2.5rem)]"
            style={{ fontWeight: 800 }}
          >
            Certificaciones CELAC
          </h2>
          <p className="text-[#29235C]/50 text-[16px] mt-4 max-w-2xl mx-auto">
            Contamos con certificaciones de calidad en educación otorgadas por CELAC, que avalan nuestros programas bajo estándares nacionales e internacionales.
          </p>
        </div>

        {/* Desktop: grid */}
        <div className="hidden md:grid md:grid-cols-3 lg:grid-cols-6 gap-6 justify-items-center">
          {certificates.map((cert) => (
            <div
              key={cert.alt}
              className="bg-white rounded-xl p-4 shadow-sm hover:shadow-lg hover:shadow-[#29235C]/5 transition-all duration-300 flex items-center justify-center"
            >
              <img
                src={cert.src}
                alt={cert.alt}
                className="h-40 w-auto object-contain"
                loading="lazy"
              />
            </div>
          ))}
        </div>

        {/* Mobile: Swiper carousel */}
        <div className="md:hidden">
          <Swiper
            modules={[Autoplay, Pagination]}
            slidesPerView={2}
            spaceBetween={16}
            autoplay={{ delay: 2500, disableOnInteraction: false }}
            pagination={{ clickable: true }}
            loop
            className="celac-swiper pb-10"
          >
            {certificates.map((cert) => (
              <SwiperSlide key={cert.alt}>
                <div className="bg-white rounded-xl p-4 shadow-sm flex items-center justify-center">
                  <img
                    src={cert.src}
                    alt={cert.alt}
                    className="h-36 w-auto object-contain"
                    loading="lazy"
                  />
                </div>
              </SwiperSlide>
            ))}
          </Swiper>
        </div>
      </div>
    </section>
  );
}
