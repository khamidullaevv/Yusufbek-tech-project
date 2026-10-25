import type { Estimate, MarketName } from "@/lib/api";

type ResultCardProps = {
  estimate: Estimate;
};

const formatMoney = (amount: number) =>
  `${new Intl.NumberFormat("ru-RU").format(amount)} сум`;

const markets: MarketName[] = ["Джами", "Куйлюк"];

export default function ResultCard({ estimate }: ResultCardProps) {
  return (
    <section
      aria-live="polite"
      className="overflow-hidden rounded-3xl border border-white/10 bg-panel shadow-2xl shadow-black/20"
    >
      <div className="border-b border-white/10 bg-gradient-to-br from-[#14273a] to-panel p-6 sm:p-8">
        <div className="flex items-center justify-between gap-4">
          <p className="text-sm font-medium text-slate-400">Ориентировочная смета</p>
          <span className="rounded-full border border-mint/20 bg-mint/10 px-3 py-1 text-xs font-medium text-mint">
            {estimate.repair_type}
          </span>
        </div>
        <p className="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
          {formatMoney(estimate.total_uzs)}
        </p>
        <p className="mt-2 text-sm text-slate-400">
          Материалы для квартиры площадью {estimate.area_sqm} м²
        </p>

        <div className="mt-6 grid grid-cols-2 gap-3">
          {markets.map((market) => (
            <div
              key={market}
              className="rounded-2xl border border-white/10 bg-white/[0.035] p-4"
            >
              <p className="text-xs text-slate-400">На рынке {market}</p>
              <p className="mt-1 text-sm font-semibold text-white">
                {formatMoney(estimate.market_totals_uzs[market])}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="p-6 sm:p-8">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="font-semibold text-white">Материалы</h2>
          <span className="text-xs text-slate-500">Средняя цена за единицу</span>
        </div>
        <ul className="divide-y divide-white/[0.07]">
          {estimate.materials.map((material) => (
            <li
              key={material.id}
              className="flex items-center justify-between gap-4 py-4 first:pt-0 last:pb-0"
            >
              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-slate-100">
                  {material.name}
                </p>
                <p className="mt-1 text-xs text-slate-500">
                  {material.quantity} {material.unit} ·{" "}
                  {formatMoney(material.average_unit_price_uzs)} / {material.unit}
                </p>
                <p className="mt-1 text-[11px] text-slate-600">
                  Джами {formatMoney(material.market_prices["Джами"])} · Куйлюк{" "}
                  {formatMoney(material.market_prices["Куйлюк"])}
                </p>
              </div>
              <p className="shrink-0 text-sm font-semibold text-white">
                {formatMoney(material.total_uzs)}
              </p>
            </li>
          ))}
        </ul>
        <p className="mt-6 rounded-xl bg-white/[0.035] px-4 py-3 text-xs leading-5 text-slate-500">
          Расчёт ориентировочный: фактический расход зависит от планировки и
          состояния поверхностей.
        </p>
      </div>
    </section>
  );
}
