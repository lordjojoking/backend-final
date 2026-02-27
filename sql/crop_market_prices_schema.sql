-- ============================================================
-- TABLE: crop_market_prices
-- Purpose: Store historical crop market prices from Dataset API
-- ============================================================

CREATE TABLE IF NOT EXISTS public.crop_market_prices (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    crop_id            UUID NOT NULL,
    crop_name          TEXT NOT NULL,
    market_name        TEXT NOT NULL,
    price_per_quintal  NUMERIC(10, 2) NOT NULL CHECK (price_per_quintal >= 0),
    date               DATE NOT NULL,
    synced_at          TIMESTAMPTZ DEFAULT NOW(),
    created_at         TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- UNIQUE CONSTRAINT: prevent duplicate rows per crop+market+date
-- ============================================================
ALTER TABLE public.crop_market_prices
    ADD CONSTRAINT uq_crop_market_date
    UNIQUE (crop_id, market_name, date);

-- ============================================================
-- INDEXES
-- ============================================================

-- Primary lookup pattern: filter by crop_id + date range
CREATE INDEX IF NOT EXISTS idx_crop_market_crop_date
    ON public.crop_market_prices (crop_id, date DESC);

-- Optional: lookup by crop_name for flexible searches
CREATE INDEX IF NOT EXISTS idx_crop_market_name_date
    ON public.crop_market_prices (crop_name, date DESC);

-- ============================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================

ALTER TABLE public.crop_market_prices ENABLE ROW LEVEL SECURITY;

-- Allow all authenticated users to read market prices
CREATE POLICY "Market prices are readable by all authenticated users"
    ON public.crop_market_prices
    FOR SELECT
    TO authenticated
    USING (true);

-- Allow unauthenticated (anon) users to read market prices too
-- (needed because React Native anon key is used on frontend)
CREATE POLICY "Market prices are readable by anon role"
    ON public.crop_market_prices
    FOR SELECT
    TO anon
    USING (true);

-- Only service_role (Edge Functions) can insert/update/delete
CREATE POLICY "Only service role can write market prices"
    ON public.crop_market_prices
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- ============================================================
-- OPTIONAL: table to track last sync time per crop
-- ============================================================
CREATE TABLE IF NOT EXISTS public.market_sync_log (
    crop_id        UUID PRIMARY KEY,
    crop_name      TEXT NOT NULL,
    last_synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE public.market_sync_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Sync log readable by authenticated"
    ON public.market_sync_log FOR SELECT TO authenticated USING (true);

CREATE POLICY "Sync log readable by anon"
    ON public.market_sync_log FOR SELECT TO anon USING (true);

CREATE POLICY "Only service role writes sync log"
    ON public.market_sync_log FOR ALL TO service_role
    USING (true) WITH CHECK (true);
