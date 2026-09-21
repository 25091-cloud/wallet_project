from rest_framework import serializers
from .models import transaction
from wallet.models import wallet


class TransactionSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لعرض المعاملات
    
    📌 الحقول المضافة:
    - Operation: نوع العملية من وجهة نظر المستخدم الحالي
    - telephone_expediteur: رقم هاتف المرسل
    - telephone_destinataire: رقم هاتف المستقبل
    """
    
    # 🔍 حقل حسابي لعرض نوع العملية
    Operation = serializers.SerializerMethodField()
    
    # 🔍 حقول حسابية لعرض أرقام الهواتف بدلاً من IDs
    telephone_expediteur = serializers.SerializerMethodField()
    telephone_destinataire = serializers.SerializerMethodField()

    class Meta:
        model = transaction
        fields = [
            'trans_id',
            'montant',
            'date_trans',
            'type_trans',
            'Operation',  # ✅ تم التصحيح: كان "get_type_trans"
            'statut_trans',
            'telephone_expediteur',
            'telephone_destinataire',
        ]
        read_only_fields = fields

    def get_Operation(self, obj):
        """
        ✅ تم التصحيح: تحديد نوع العملية من وجهة نظر المستخدم الحالي
        
        📌 المنطق:
        - إذا كان المستخدم هو المرسل → "تحويل صادر" أو "سحب"
        - إذا كان المستخدم هو المستقبل → "تحويل وارد"
        - إذا كان الإيداع → "إيداع"
        """
        request = self.context.get('request')
        if not request or not request.user:
            return obj.type_trans
        
        current_user = request.user
        
        # 📌 حالة الإيداع
        if obj.type_trans == "depot":
            return "depot"
        
        # 📌 حالة السحب
        if obj.type_trans == "retrait":
            return "retrait"
        
        # 📌 حالة التحويل
        if obj.type_trans == "transfert":
            # ✅ التحقق من أن المحفظة تعود للمستخدم الحالي
            if obj.wallet_expediteur and obj.wallet_expediteur.user == current_user:
                return "envoi"
            elif obj.wallet_destinataire and obj.wallet_destinataire.user == current_user:
                return "recoit"
        
        return obj.type_trans

    def get_telephone_expediteur(self, obj):
        """
        ✅ استخراج رقم هاتف المرسل بدلاً من عرض ID المحفظة
        
        📌 الحالات:
        - إذا لم تكن هناك محفظة مرسلة → None
        - وإلا → رقم هاتف المستخدم المرتبط بالمحفظة
        """
        if not obj.wallet_expediteur:
            return None
        return obj.wallet_expediteur.user.nb_telephone

    def get_telephone_destinataire(self, obj):
        """
        ✅ استخراج رقم هاتف المستقبل بدلاً من عرض ID المحفظة
        """
        if not obj.wallet_destinataire:
            return None
        return obj.wallet_destinataire.user.nb_telephone

    
