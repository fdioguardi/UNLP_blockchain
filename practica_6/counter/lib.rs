#![cfg_attr(not(feature = "std"), no_std, no_main)]

#[ink::contract]
mod counter {
    use ink::storage::Mapping;

    #[ink(storage)]
    pub struct Counter {
        value: u128,
        owner: AccountId,
        whitelist: Mapping<AccountId, bool>,
    }

    #[ink(event)]
    pub struct Decrement {
        #[ink(topic)]
        by: AccountId,
        new_value: u128,
    }

    #[ink(event)]
    pub struct Increment {
        #[ink(topic)]
        by: AccountId,
        new_value: u128,
    }

    impl Counter {
        #[ink(constructor)]
        pub fn new() -> Self {
            let mut whitelist = Mapping::default();
            let owner = Self::env().caller();
            whitelist.insert(owner, &true);
            Self {
                value: 0,
                owner,
                whitelist
            }
        }

        #[ink(message)]
        pub fn add_to_whitelist(&mut self, account: AccountId) {
            self.only_owner();
            self.whitelist.insert(account, &true);
        }

        #[ink(message)]
        pub fn remove_from_whitelist(&mut self, account: AccountId) {
            self.only_owner();
            self.whitelist.remove(account);
        }

        #[ink(message)]
        pub fn increment(&mut self) {
            self.only_whitelisted();
            self.value = self.value.wrapping_add(1);
            self.env().emit_event(Increment {
                by: self.env().caller(),
                new_value: self.value,
            });
        }

        #[ink(message)]
        pub fn decrement(&mut self) {
            self.only_whitelisted();
            self.value = self.value.wrapping_sub(1);
            self.env().emit_event(Decrement {
                by: self.env().caller(),
                new_value: self.value,
            });
        }

        #[ink(message)]
        pub fn get_counter(&self) -> u128 {
            self.value
        }

        fn only_whitelisted(&self) {
            assert!(self.whitelist.get(self.env().caller()).unwrap_or(false), "Not authorized: not in the whitelist");
        }

        fn only_owner(&self) {
            assert_eq!(self.env().caller(), self.owner, "Only owner can manage the whitelist");
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[ink::test]
        fn test_increment_and_decrement() {
            let mut contract = Counter::new();
            contract.increment();
            assert_eq!(contract.get_counter(), 1);
            contract.decrement();
            assert_eq!(contract.get_counter(), 0);
        }

        #[ink::test]
        fn test_whitelist() {
            let mut contract = Counter::new();
            let user = AccountId::from([0x02; 32]);

            contract.add_to_whitelist(user);
            assert!(contract.whitelist.get(user).unwrap_or(false));

            contract.remove_from_whitelist(user);
            assert!(!contract.whitelist.get(user).unwrap_or(false));
        }
    }


    // /// This is how you'd write end-to-end (E2E) or integration tests for ink! contracts.
    // ///
    // /// When running these you need to make sure that you:
    // /// - Compile the tests with the `e2e-tests` feature flag enabled (`--features e2e-tests`)
    // /// - Are running a Substrate node which contains `pallet-contracts` in the background
    // #[cfg(all(test, feature = "e2e-tests"))]
    // mod e2e_tests {
    //     /// Imports all the definitions from the outer scope so we can use them here.
    //     use super::*;

    //     /// A helper function used for calling contract messages.
    //     use ink_e2e::build_message;

    //     /// The End-to-End test `Result` type.
    //     type E2EResult<T> = std::result::Result<T, Box<dyn std::error::Error>>;

    //     /// We test that we can upload and instantiate the contract using its default constructor.
    //     #[ink_e2e::test]
    //     async fn default_works(mut client: ink_e2e::Client<C, E>) -> E2EResult<()> {
    //         // Given
    //         let constructor = CounterRef::default();

    //         // When
    //         let contract_account_id = client
    //             .instantiate("counter", &ink_e2e::alice(), constructor, 0, None)
    //             .await
    //             .expect("instantiate failed")
    //             .account_id;

    //         // Then
    //         let get = build_message::<CounterRef>(contract_account_id.clone())
    //             .call(|counter| counter.get());
    //         let get_result = client.call_dry_run(&ink_e2e::alice(), &get, 0, None).await;
    //         assert!(matches!(get_result.return_value(), false));

    //         Ok(())
    //     }

    //     /// We test that we can read and write a value from the on-chain contract contract.
    //     #[ink_e2e::test]
    //     async fn it_works(mut client: ink_e2e::Client<C, E>) -> E2EResult<()> {
    //         // Given
    //         let constructor = CounterRef::new(false);
    //         let contract_account_id = client
    //             .instantiate("counter", &ink_e2e::bob(), constructor, 0, None)
    //             .await
    //             .expect("instantiate failed")
    //             .account_id;

    //         let get = build_message::<CounterRef>(contract_account_id.clone())
    //             .call(|counter| counter.get());
    //         let get_result = client.call_dry_run(&ink_e2e::bob(), &get, 0, None).await;
    //         assert!(matches!(get_result.return_value(), false));

    //         // When
    //         let flip = build_message::<CounterRef>(contract_account_id.clone())
    //             .call(|counter| counter.flip());
    //         let _flip_result = client
    //             .call(&ink_e2e::bob(), flip, 0, None)
    //             .await
    //             .expect("flip failed");

    //         // Then
    //         let get = build_message::<CounterRef>(contract_account_id.clone())
    //             .call(|counter| counter.get());
    //         let get_result = client.call_dry_run(&ink_e2e::bob(), &get, 0, None).await;
    //         assert!(matches!(get_result.return_value(), true));

    //         Ok(())
    //     }
    // }
}
