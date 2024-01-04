from django import forms
from django.forms import ModelForm,TextInput,Textarea,ClearableFileInput,CheckboxInput,DateTimeInput,ModelChoiceField
from .models import User,Category,AuctionList,Bid,WatchList,AuctionComment


class CreateListingForm(ModelForm):
    required_css_class='required'


    categoryid=forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select({'class':'form-control'}),
        label='Category'
    )

    class Meta:
        model = AuctionList
        fields=('title','description','categoryid','image','price','isactive')
       
        widgets ={
            'title': TextInput(),
            'description': Textarea( attrs={'rows':'4'}),
            'image': ClearableFileInput(),
            'price': TextInput(),
            'isactive': CheckboxInput()
        }
        
        # Specify common attributes for all widgets
        attrs = {'class': 'form-control'}
        for field in widgets:
            widgets[field].attrs.update(attrs)
     

class BidForm(ModelForm):
    def __init__(self, *args, **kwargs):
        existing_bidprice = kwargs.pop('existing_bidprice', None)
        page_message_error = kwargs.pop('page_message_error', None)
        page_message_success = kwargs.pop('page_message_success', None)
        super(BidForm, self).__init__(*args, **kwargs)
        self.existing_bidprice=existing_bidprice
        self.page_message_error=page_message_error
        self.page_message_success=page_message_success

    required_css_class='required'

    auctionid=forms.ModelChoiceField(
        queryset=AuctionList.objects.filter(isactive=True),
        required=False,
        widget=forms.Select({'class':'form-control'}),
        label='AuctionList'
    )

    userid=forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        widget=forms.Select({'class':'form-control'}),
        label='User'
    )

    class Meta:
        model = Bid
        fields=('auctionid','userid','bidprice')

        widgets ={
            'bidprice': TextInput()
        }

        # Specify common attributes for all widgets
        attrs = {'class': 'form-control'}
        for field in widgets:
            widgets[field].attrs.update(attrs)


    #Custom validation
    def clean_bidprice(self):
        bidprice=self.cleaned_data.get('bidprice')
        existing_bidprice=self.existing_bidprice

        if bidprice and bidprice <= existing_bidprice:
            raise forms.ValidationError('Bid must be greater than existing bid price')

        
        return bidprice
    


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': TextInput(attrs={'required': 'required'}),
            'email': TextInput(attrs={'required': 'required'}),
            'first_name': TextInput(attrs={'required': 'required'})
        }




        
