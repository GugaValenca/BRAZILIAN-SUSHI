import { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { ArrowRight, Clock, MapPin, Minus, Plus, ShoppingBag, Trash2 } from "lucide-react";
import { toast } from "sonner";

import SectionHeading from "@/components/SectionHeading";
import { useCart } from "@/contexts/CartContext";
import { createOrder, fetchDeliveryZones } from "@/lib/catalog";

const CheckoutPage = () => {
  const navigate = useNavigate();
  const { items, subtotal, updateQuantity, removeItem, clearCart } = useCart();
  const [orderType, setOrderType] = useState<"delivery" | "pickup">("delivery");
  const [guestName, setGuestName] = useState("");
  const [guestEmail, setGuestEmail] = useState("");
  const [guestPhone, setGuestPhone] = useState("");
  const [notes, setNotes] = useState("");
  const [allergyNotes, setAllergyNotes] = useState("");
  const [notificationPreference, setNotificationPreference] = useState<"sms" | "email" | "both">("both");
  const [deliveryZoneId, setDeliveryZoneId] = useState<number | undefined>(undefined);

  const { data: deliveryZones } = useQuery({
    queryKey: ["delivery-zones"],
    queryFn: fetchDeliveryZones,
  });

  const selectedZone = useMemo(
    () => deliveryZones?.find((zone) => zone.id === deliveryZoneId),
    [deliveryZoneId, deliveryZones],
  );

  const deliveryFee = orderType === "delivery" ? Number(selectedZone?.fee ?? 0) : 0;
  const total = subtotal + deliveryFee;

  const orderMutation = useMutation({
    mutationFn: createOrder,
    onSuccess: (order) => {
      clearCart();
      toast.success("Order placed successfully");
      navigate(`/track-order?order=${order.id}&token=${order.tracking_token}`);
    },
    onError: () => {
      toast.error("We could not place your order right now.");
    },
  });

  const canSubmit = items.length > 0 && guestName && guestEmail && guestPhone && (orderType === "pickup" || deliveryZoneId);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!canSubmit) return;

    orderMutation.mutate({
      order_type: orderType,
      delivery_zone: orderType === "delivery" ? deliveryZoneId : undefined,
      guest_name: guestName,
      guest_email: guestEmail,
      guest_phone: guestPhone,
      notes,
      allergy_notes: allergyNotes,
      notification_preference: notificationPreference,
      items: items.map((entry) => ({
        menu_item_id: entry.item.apiId,
        quantity: entry.quantity,
      })),
    });
  };

  return (
    <div className="min-h-screen pt-24 md:pt-28 pb-16">
      <div className="container">
        <SectionHeading
          label="Checkout"
          title="Complete Your Order"
          subtitle="Review your cart, choose delivery or pickup, and send your order directly to the backend."
        />

        {items.length === 0 ? (
          <div className="max-w-2xl mx-auto bg-card border border-border rounded-2xl p-10 text-center">
            <ShoppingBag className="w-12 h-12 text-primary mx-auto mb-4" />
            <h2 className="text-2xl font-display font-bold mb-3">Your cart is empty</h2>
            <p className="text-muted-foreground mb-6">Add a few items from the menu to start a delivery or pickup order.</p>
            <Link to="/menu" className="inline-flex items-center gap-2 bg-gradient-gold text-primary-foreground px-6 py-3 rounded-lg font-semibold">
              Browse Menu <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 xl:grid-cols-[1.3fr_0.9fr] gap-8 max-w-6xl mx-auto">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="bg-card border border-border rounded-2xl p-6">
                <h3 className="text-xl font-display font-bold mb-4">Order Type</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <button type="button" onClick={() => setOrderType("delivery")} className={`rounded-xl border p-4 text-left ${orderType === "delivery" ? "border-primary bg-primary/5" : "border-border"}`}>
                    <span className="font-semibold">Delivery</span>
                    <p className="text-sm text-muted-foreground mt-1">Have it sent to your address.</p>
                  </button>
                  <button type="button" onClick={() => setOrderType("pickup")} className={`rounded-xl border p-4 text-left ${orderType === "pickup" ? "border-primary bg-primary/5" : "border-border"}`}>
                    <span className="font-semibold">Pickup</span>
                    <p className="text-sm text-muted-foreground mt-1">Skip delivery fees and pick it up yourself.</p>
                  </button>
                </div>
              </div>

              <div className="bg-card border border-border rounded-2xl p-6 space-y-4">
                <h3 className="text-xl font-display font-bold">Guest Details</h3>
                <div className="grid sm:grid-cols-2 gap-4">
                  <input value={guestName} onChange={(e) => setGuestName(e.target.value)} required placeholder="Full name" className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm" />
                  <input value={guestPhone} onChange={(e) => setGuestPhone(e.target.value)} required placeholder="Phone number" className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm" />
                </div>
                <input value={guestEmail} onChange={(e) => setGuestEmail(e.target.value)} required type="email" placeholder="Email address" className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm" />
                <div className="grid sm:grid-cols-2 gap-4">
                  <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={3} placeholder="Order notes or special requests" className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm resize-none" />
                  <textarea value={allergyNotes} onChange={(e) => setAllergyNotes(e.target.value)} rows={3} placeholder="Allergies or dietary warnings" className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm resize-none" />
                </div>
              </div>

              <div className="bg-card border border-border rounded-2xl p-6 space-y-4">
                <h3 className="text-xl font-display font-bold">Notifications</h3>
                <div className="grid sm:grid-cols-3 gap-3">
                  {([
                    ["sms", "SMS"],
                    ["email", "Email"],
                    ["both", "SMS + Email"],
                  ] as const).map(([value, label]) => (
                    <button
                      key={value}
                      type="button"
                      onClick={() => setNotificationPreference(value)}
                      className={`rounded-xl border px-4 py-3 text-sm font-medium ${notificationPreference === value ? "border-primary bg-primary/5" : "border-border"}`}
                    >
                      {label}
                    </button>
                  ))}
                </div>
              </div>

              {orderType === "delivery" && (
                <div className="bg-card border border-border rounded-2xl p-6 space-y-4">
                  <h3 className="text-xl font-display font-bold">Delivery Zone</h3>
                  <div className="grid sm:grid-cols-2 gap-4">
                    {deliveryZones?.map((zone) => (
                      <button
                        key={zone.id}
                        type="button"
                        onClick={() => setDeliveryZoneId(zone.id)}
                        className={`rounded-xl border p-4 text-left ${deliveryZoneId === zone.id ? "border-primary bg-primary/5" : "border-border"}`}
                      >
                        <div className="flex items-center justify-between gap-4">
                          <div>
                            <p className="font-semibold">{zone.name}</p>
                            <p className="text-sm text-muted-foreground flex items-center gap-2 mt-1"><MapPin className="w-4 h-4" /> {zone.postal_code}</p>
                          </div>
                          <div className="text-right">
                            <p className="font-semibold">${Number(zone.fee).toFixed(2)}</p>
                            <p className="text-sm text-muted-foreground flex items-center gap-1"><Clock className="w-4 h-4" /> {zone.average_minutes} min</p>
                          </div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <button type="submit" disabled={!canSubmit || orderMutation.isPending} className="w-full bg-gradient-gold text-primary-foreground py-4 rounded-xl font-semibold disabled:opacity-70">
                {orderMutation.isPending ? "Placing order..." : "Place Order"}
              </button>
            </form>

            <aside className="bg-card border border-border rounded-2xl p-6 h-fit sticky top-28">
              <h3 className="text-xl font-display font-bold mb-5">Order Summary</h3>
              <div className="space-y-4">
                {items.map((entry) => (
                  <div key={entry.item.id} className="border-b border-border pb-4">
                    <div className="flex gap-4">
                      <img src={entry.item.image} alt={entry.item.name} className="w-20 h-20 rounded-lg object-cover" />
                      <div className="flex-1">
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <p className="font-semibold">{entry.item.name}</p>
                            <p className="text-sm text-muted-foreground">${entry.item.price.toFixed(2)} each</p>
                          </div>
                          <button type="button" onClick={() => removeItem(entry.item.id)} className="text-muted-foreground hover:text-destructive">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                        <div className="flex items-center justify-between mt-3">
                          <div className="inline-flex items-center border border-border rounded-lg overflow-hidden">
                            <button type="button" onClick={() => updateQuantity(entry.item.id, entry.quantity - 1)} className="px-3 py-2"><Minus className="w-4 h-4" /></button>
                            <span className="px-3 text-sm font-medium">{entry.quantity}</span>
                            <button type="button" onClick={() => updateQuantity(entry.item.id, entry.quantity + 1)} className="px-3 py-2"><Plus className="w-4 h-4" /></button>
                          </div>
                          <span className="font-semibold">${(entry.item.price * entry.quantity).toFixed(2)}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="space-y-3 mt-6 text-sm">
                <div className="flex justify-between"><span className="text-muted-foreground">Subtotal</span><span>${subtotal.toFixed(2)}</span></div>
                <div className="flex justify-between"><span className="text-muted-foreground">Delivery fee</span><span>${deliveryFee.toFixed(2)}</span></div>
                <div className="flex justify-between text-base font-semibold pt-3 border-t border-border"><span>Total</span><span>${total.toFixed(2)}</span></div>
              </div>
            </aside>
          </div>
        )}
      </div>
    </div>
  );
};

export default CheckoutPage;
