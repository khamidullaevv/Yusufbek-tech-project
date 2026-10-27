"use client";

import { FormEvent, useState } from "react";
import ResultCard from "@/components/ResultCard";
import { calculateEstimate, type Estimate } from "@/lib/api";

const repairTypes: Estimate["repair_type"][] = [
  "Косметический",
  "Капитальный",
];

export default function HomePage() {
  const [area, setArea] = useState("60");
  const [repairType, setRepairType] =
    useState<Estimate["repair_type"]>("Косметический");
  const [estimate, setEstimate] = useState<Estimate | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const result = await calculateEstimate(Number(area), repairType);
      setEstimate(result);
    } catch {
      setError("Не удалось связаться с калькулятором. Проверьте, запущен ли backend.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen overflow-hidden">
      <div className="pointer-events-none absolute inset-x-0 top-0 -z-0 h-[520px] bg-[radial-gradient(ellipse_at_top,rgba(33,91,106,0.25),transparent_65%)]" />
      <div className="relative mx-auto max-w-6xl px-5 pb-16 pt-6 sm:px-8 sm:pt-10">
        <header className="flex items-center justify-between">
          <a href="#" className="flex items-center gap-2.5" aria-label="StroyFix — главная">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-mint text-midnight">
              <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5" aria-hidden="true">
                <path
                  d="M4 11.5 12 5l8 6.5v7a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 18.5v-7Z"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinejoin="round"
                />
                <path d="M9 20v-6h6v6" stroke="currentColor" strokeWidth="1.8" />
              </svg>
            </span>
            <span className="text-lg font-semibold tracking-tight">StroyFix</span>
          </a>
          <span className="rounded-full border border-white/10 px-3 py-1.5 text-xs text-slate-400">
            Ташкент · Узбекистан
          </span>
        </header>

        <section className="mx-auto mb-10 mt-14 max-w-2xl text-center sm:mb-12 sm:mt-20">
          <div className="mx-auto mb-5 inline-flex items-center gap-2 rounded-full border border-mint/15 bg-mint/[0.07] px-3 py-1.5 text-xs text-mint">
            <span className="h-1.5 w-1.5 rounded-full bg-mint" />
            Бесплатно · Без регистрации
          </div>
          <h1 className="text-4xl font-semibold leading-tight tracking-tight text-white sm:text-5xl">
            Ремонт начинается
            <br className="hidden sm:block" /> с точного расчёта
          </h1>
          <p className="mx-auto mt-4 max-w-lg text-sm leading-6 text-slate-400 sm:text-base">
            Узнайте примерную стоимость материалов и сравните цены на рынках
            Ташкента за минуту.
          </p>
        </section>

        <div className="mx-auto grid max-w-5xl items-start gap-6 lg:grid-cols-[0.8fr_1.2fr]">
          <section className="rounded-3xl border border-white/10 bg-panel p-6 shadow-2xl shadow-black/20 sm:p-8">
            <div className="mb-7">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-mint">
                Ваш проект
              </p>
              <h2 className="mt-2 text-xl font-semibold text-white">
                Пара деталей о ремонте
              </h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label
                  htmlFor="area"
                  className="mb-2 block text-sm font-medium text-slate-300"
                >
                  Площадь квартиры
                </label>
                <div className="relative">
                  <input
                    id="area"
                    type="number"
                    min="1"
                    max="1000"
                    step="0.1"
                    required
                    value={area}
                    onChange={(event) => setArea(event.target.value)}
                    className="w-full rounded-xl border border-white/10 bg-[#0b1523] px-4 py-3.5 pr-14 text-white outline-none transition placeholder:text-slate-600 focus:border-mint/50 focus:ring-2 focus:ring-mint/10"
                    placeholder="Например, 60"
                  />
                  <span className="absolute right-4 top-1/2 -translate-y-1/2 text-sm text-slate-500">
                    м²
                  </span>
                </div>
                <p className="mt-2 text-xs text-slate-500">
                  Укажите площадь от 1 до 1000 кубетных метров. Если площадь квартиры известна в квадратных метрах, укажите её напрямую.
                </p>
              </div>

              <fieldset>
                <legend className="mb-2 block text-sm font-medium text-slate-300">
                  Тип ремонта
                </legend>
                <div className="grid grid-cols-2 gap-3">
                  {repairTypes.map((type) => {
                    const active = repairType === type;
                    return (
                      <button
                        key={type}
                        type="button"
                        aria-pressed={active}
                        onClick={() => setRepairType(type)}
                        className={`rounded-xl border px-3 py-3.5 text-sm font-medium transition ${
                          active
                            ? "border-mint/50 bg-mint/[0.08] text-mint"
                            : "border-white/10 bg-[#0b1523] text-slate-400 hover:border-white/20 hover:text-slate-200"
                        }`}
                      >
                        {type}
                      </button>
                    );
                  })}
                </div>
              </fieldset>

              {error && (
                <p role="alert" className="rounded-xl bg-red-400/10 px-4 py-3 text-sm text-red-300">
                  {error}
                </p>
              )}

              <button
                type="submit"
                disabled={loading}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-mint px-5 py-3.5 font-semibold text-midnight transition hover:bg-[#70ebc3] disabled:cursor-wait disabled:opacity-70"
              >
                {loading ? "Считаем смету..." : "Рассчитать смету"}
                {!loading && (
                  <svg viewBox="0 0 20 20" fill="none" className="h-4 w-4" aria-hidden="true">
                    <path
                      d="M4 10h12m-5-5 5 5-5 5"
                      stroke="currentColor"
                      strokeWidth="1.7"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                )}
              </button>
            </form>

            <div className="mt-6 flex items-start gap-3 border-t border-white/[0.07] pt-5">
              <svg viewBox="0 0 20 20" fill="none" className="mt-0.5 h-4 w-4 shrink-0 text-slate-500" aria-hidden="true">
                <path
                  d="M10 2.5 4 5v4.2c0 3.8 2.6 6.6 6 8.3 3.4-1.7 6-4.5 6-8.3V5l-6-2.5Z"
                  stroke="currentColor"
                  strokeWidth="1.4"
                  strokeLinejoin="round"
                />
                <path d="m7.5 10 1.7 1.7 3.5-3.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
              </svg>
              <p className="text-xs leading-5 text-slate-500">
                Ваши данные не сохраняются. Расчёт работает без регистрации.
              </p>
            </div>
          </section>

          <div>
            {estimate ? (
              <ResultCard estimate={estimate} />
            ) : (
              <div className="flex min-h-[340px] flex-col items-center justify-center rounded-3xl border border-dashed border-white/10 bg-white/[0.015] px-8 text-center sm:min-h-[460px]">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-white/10 bg-panel text-mint">
                  <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6" aria-hidden="true">
                    <path d="M5 19h14M7 16V9m5 7V5m5 11v-4" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" />
                  </svg>
                </div>
                <h2 className="mt-5 font-medium text-slate-200">
                  Здесь появится ваша смета
                </h2>
                <p className="mt-2 max-w-xs text-sm leading-6 text-slate-500">
                  Укажите площадь и тип ремонта — мы покажем расход материалов и сравним цены.
                </p>
              </div>
            )}
          </div>
        </div>

        <footer className="mt-12 text-center text-xs text-slate-600">
          StroyFix · Ориентировочные цены на материалы в Ташкенте
        </footer>
      </div>
    </main>
  );
}
